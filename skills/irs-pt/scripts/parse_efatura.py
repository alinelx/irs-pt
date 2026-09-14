#!/usr/bin/env python3
"""Lê exportações CSV do portal e-Fatura e agrega-as.

Não decide dedutibilidade. Reporta o que está no ficheiro, corrige o sinal das
notas de crédito e assinala o que não conseguiu classificar. Os valores da
Autoridade Tributária prevalecem sempre sobre este output.

Uso:
    python3 parse_efatura.py FICHEIRO.csv --resumo
    python3 parse_efatura.py *.csv --ano 2025 --json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

AVISO_LINHAS = 300

ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")
DELIMITADORES = (";", ",", "\t", "|")

# Nomes de coluna conhecidos, já normalizados (minúsculas, sem acentos).
CAMPOS = {
    "data": ("data emissao", "data de emissao", "data do documento", "data documento", "data"),
    "nif_emitente": ("nif emitente", "nif do emitente", "nif comerciante", "contribuinte emitente", "nif"),
    "nome_emitente": ("nome emitente", "nome do emitente", "designacao emitente", "comerciante", "emitente", "nome"),
    "tipo": ("tipo de documento", "tipo documento", "tipo doc", "tipo"),
    "setor": ("setor de atividade", "sector de actividade", "setor economico", "setor", "sector", "atividade", "actividade"),
    "situacao": ("situacao do documento", "situacao da fatura", "estado do documento", "situacao", "estado"),
    "total": ("valor total", "total com iva", "total c/ iva", "valor com iva", "montante total", "valor", "total"),
    "iva": ("valor do iva", "valor iva", "total iva", "iva"),
    "base": ("base tributavel", "valor tributavel", "valor sem iva", "valor s/ iva", "base"),
    "afetacao": ("afetacao", "afectacao", "atividade profissional", "afeto a atividade", "ambito", "utilizacao"),
}

RE_CREDITO = re.compile(r"\b(nota\s*de\s*cr|nc\b|credito|devolu)", re.I)
RE_ANULADO = re.compile(r"\banulad", re.I)
RE_PENDENTE = re.compile(r"(pendente|falta|aguard|por\s*valid|por\s*classific|incomplet)", re.I)


def sem_acentos(texto: str) -> str:
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def normaliza_cabecalho(nome: str) -> str:
    limpo = sem_acentos((nome or "").strip().lower())
    limpo = limpo.replace("º", "").replace("ª", "").replace("nº", "n")
    limpo = re.sub(r"[^a-z0-9/ ]+", " ", limpo)
    return re.sub(r"\s+", " ", limpo).strip()


def le_texto(caminho: Path) -> str:
    dados = caminho.read_bytes()
    for enc in ENCODINGS:
        try:
            return dados.decode(enc)
        except UnicodeDecodeError:
            continue
    return dados.decode("latin-1", errors="replace")


def deteta_delimitador(amostra: str) -> str:
    try:
        return csv.Sniffer().sniff(amostra, delimiters="".join(DELIMITADORES)).delimiter
    except csv.Error:
        pass
    # Fallback: o delimitador mais frequente na linha mais "densa".
    melhor, contagem = ";", 0
    for delim in DELIMITADORES:
        n = max((linha.count(delim) for linha in amostra.splitlines()[:20]), default=0)
        if n > contagem:
            melhor, contagem = delim, n
    return melhor


def encontra_cabecalho(linhas: list[list[str]]) -> int:
    """Devolve o índice da linha de cabeçalho, saltando preâmbulos."""
    conhecidos = {alias for aliases in CAMPOS.values() for alias in aliases}
    for i, linha in enumerate(linhas[:25]):
        normalizadas = {normaliza_cabecalho(c) for c in linha}
        if len(normalizadas & conhecidos) >= 2:
            return i
    return 0


def mapeia_colunas(cabecalho: list[str]) -> dict[str, int]:
    normalizado = [normaliza_cabecalho(c) for c in cabecalho]
    mapa: dict[str, int] = {}
    for campo, aliases in CAMPOS.items():
        for alias in aliases:  # ordem = prioridade
            for i, nome in enumerate(normalizado):
                if nome == alias and i not in mapa.values():
                    mapa[campo] = i
                    break
            if campo in mapa:
                break
        if campo not in mapa:  # segunda passagem, correspondência parcial
            for alias in aliases:
                for i, nome in enumerate(normalizado):
                    if alias in nome and i not in mapa.values():
                        mapa[campo] = i
                        break
                if campo in mapa:
                    break
    return mapa


def parse_valor(bruto: str) -> float:
    """Converte número em formato português ('1.234,56 €') para float."""
    if bruto is None:
        return 0.0
    texto = sem_acentos(str(bruto)).strip()
    texto = texto.replace("\xa0", " ").replace("EUR", "").replace("€", "").strip()
    if not texto:
        return 0.0
    negativo = texto.startswith("(") and texto.endswith(")")
    if negativo:
        texto = texto[1:-1]
    texto = re.sub(r"[^\d,.\-]", "", texto)
    if not texto or texto in {"-", ".", ","}:
        return 0.0
    if "," in texto and "." in texto:
        # O separador decimal é o que aparece mais à direita.
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        texto = texto.replace(",", ".")
    elif texto.count(".") > 1:
        texto = texto.replace(".", "")
    else:
        inteiro, _, decimal = texto.partition(".")
        if decimal and len(decimal) == 3 and len(inteiro) <= 3:
            texto = inteiro + decimal  # 1.234 = milhares, não decimais
    try:
        valor = float(texto)
    except ValueError:
        return 0.0
    return -valor if negativo else valor


FORMATOS_DATA = ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y", "%d-%m-%y", "%d/%m/%y")


def parse_data(bruto: str) -> date | None:
    texto = (bruto or "").strip()
    if not texto:
        return None
    texto = texto.split("T")[0].split(" ")[0]
    for fmt in FORMATOS_DATA:
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            continue
    return None


def le_ficheiro(caminho: Path) -> tuple[list[dict], list[str]]:
    problemas: list[str] = []
    texto = le_texto(caminho)
    if not texto.strip():
        return [], [f"{caminho.name}: ficheiro vazio"]

    delim = deteta_delimitador(texto[:8000])
    linhas = list(csv.reader(texto.splitlines(), delimiter=delim))
    linhas = [linha for linha in linhas if any(c.strip() for c in linha)]
    if not linhas:
        return [], [f"{caminho.name}: sem linhas de dados"]

    idx = encontra_cabecalho(linhas)
    cabecalho, corpo = linhas[idx], linhas[idx + 1:]
    mapa = mapeia_colunas(cabecalho)

    em_falta = [c for c in ("data", "total") if c not in mapa]
    if em_falta:
        problemas.append(
            f"{caminho.name}: não encontrei a(s) coluna(s) {', '.join(em_falta)}. "
            f"Cabeçalho lido: {', '.join(cabecalho[:12])}"
        )
        return [], problemas

    registos = []
    for n, linha in enumerate(corpo, start=idx + 2):
        def campo(nome: str) -> str:
            i = mapa.get(nome)
            return linha[i].strip() if i is not None and i < len(linha) else ""

        total = parse_valor(campo("total"))
        tipo = campo("tipo")
        situacao = campo("situacao")
        anulado = bool(RE_ANULADO.search(situacao) or RE_ANULADO.search(tipo))
        credito = bool(RE_CREDITO.search(tipo))
        # Nota de crédito abate ao total: garantir sinal negativo.
        if credito and total > 0:
            total = -total
        d = parse_data(campo("data"))
        if d is None and campo("data"):
            problemas.append(f"{caminho.name}:{n}: data ilegível ({campo('data')!r})")

        registos.append({
            "ficheiro": caminho.name,
            "linha": n,
            "data": d.isoformat() if d else None,
            "ano": d.year if d else None,
            "mes": f"{d.year}-{d.month:02d}" if d else None,
            "nif_emitente": campo("nif_emitente"),
            "nome_emitente": campo("nome_emitente") or "(sem nome)",
            "tipo": tipo or "(sem tipo)",
            "setor": campo("setor") or "(sem setor)",
            "situacao": situacao or "(sem estado)",
            "afetacao": campo("afetacao"),
            "total": round(total, 2),
            "iva": round(parse_valor(campo("iva")), 2),
            "base": round(parse_valor(campo("base")), 2),
            "nota_credito": credito,
            "anulado": anulado,
            "pendente": bool(RE_PENDENTE.search(situacao)),
        })
    return registos, problemas


def agrega(registos: list[dict]) -> dict:
    validos = [r for r in registos if not r["anulado"]]
    pendentes = [r for r in validos if r["pendente"]]
    creditos = [r for r in validos if r["nota_credito"]]

    def soma(rs): return round(sum(r["total"] for r in rs), 2)

    por_setor = defaultdict(lambda: {"n": 0, "total": 0.0})
    por_estado = defaultdict(lambda: {"n": 0, "total": 0.0})
    por_mes = defaultdict(lambda: {"n": 0, "total": 0.0})
    por_emitente = defaultdict(lambda: {"n": 0, "total": 0.0})
    for r in validos:
        for chave, destino in (
            (r["setor"], por_setor), (r["situacao"], por_estado),
            (r["mes"] or "(sem data)", por_mes), (r["nome_emitente"], por_emitente),
        ):
            destino[chave]["n"] += 1
            destino[chave]["total"] = round(destino[chave]["total"] + r["total"], 2)

    datas = sorted(r["data"] for r in validos if r["data"])
    return {
        "documentos": len(registos),
        "considerados": len(validos),
        "anulados": len(registos) - len(validos),
        "total": soma(validos),
        "total_iva": round(sum(r["iva"] for r in validos), 2),
        "intervalo": {"de": datas[0], "a": datas[-1]} if datas else None,
        "notas_credito": {"n": len(creditos), "total": soma(creditos)},
        "pendentes": {"n": len(pendentes), "total": soma(pendentes)},
        "por_setor": dict(sorted(por_setor.items(), key=lambda kv: -kv[1]["total"])),
        "por_estado": dict(sorted(por_estado.items(), key=lambda kv: -kv[1]["n"])),
        "por_mes": dict(sorted(por_mes.items())),
        "por_emitente": dict(sorted(por_emitente.items(), key=lambda kv: -kv[1]["total"])),
        "lista_pendentes": [
            {k: r[k] for k in ("data", "nome_emitente", "setor", "situacao", "total")}
            for r in sorted(pendentes, key=lambda r: r["data"] or "")
        ],
    }


def eur(v: float) -> str:
    s = f"{abs(v):,.2f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return f"{'-' if v < 0 else ''}{s} €"


def imprime_resumo(a: dict, problemas: list[str], limite_emitentes: int = 10) -> None:
    print("=" * 62)
    print("  RESUMO e-Fatura")
    print("=" * 62)
    if a["intervalo"]:
        print(f"  Período           {a['intervalo']['de']} a {a['intervalo']['a']}")
    print(f"  Documentos        {a['considerados']} considerados"
          + (f" ({a['anulados']} anulados, excluídos)" if a["anulados"] else ""))
    print(f"  Total             {eur(a['total'])}")
    print(f"  IVA               {eur(a['total_iva'])}")
    if a["notas_credito"]["n"]:
        print(f"  Notas de crédito  {a['notas_credito']['n']} · {eur(a['notas_credito']['total'])} (já abatidas)")

    if a["por_setor"]:
        print("\n--- Por setor " + "-" * 48)
        for setor, v in a["por_setor"].items():
            print(f"  {setor[:40]:<40} {v['n']:>4}  {eur(v['total']):>14}")

    if a["por_estado"]:
        print("\n--- Por estado " + "-" * 47)
        for estado, v in a["por_estado"].items():
            print(f"  {estado[:40]:<40} {v['n']:>4}  {eur(v['total']):>14}")

    if a["por_emitente"]:
        print(f"\n--- Maiores emitentes (top {limite_emitentes}) " + "-" * 27)
        for nome, v in list(a["por_emitente"].items())[:limite_emitentes]:
            print(f"  {nome[:40]:<40} {v['n']:>4}  {eur(v['total']):>14}")

    if a["pendentes"]["n"]:
        print("\n" + "!" * 62)
        print(f"  {a['pendentes']['n']} DOCUMENTO(S) PENDENTE(S) · {eur(a['pendentes']['total'])}")
        print("  Enquanto ficarem pendentes NÃO contam. Resolver no portal e-Fatura")
        print("  dentro do prazo (ver references/valores-anuais.md).")
        print("!" * 62)
        for r in a["lista_pendentes"][:20]:
            print(f"  {r['data'] or '(sem data)':<12} {r['nome_emitente'][:32]:<32} {eur(r['total']):>12}")
        if len(a["lista_pendentes"]) > 20:
            print(f"  ... e mais {len(a['lista_pendentes']) - 20}. Usar --json para a lista completa.")

    if a["considerados"] >= AVISO_LINHAS:
        print(f"\n  AVISO: {a['considerados']} documentos (limiar {AVISO_LINHAS}). Conferir por")
        print("  amostragem contra o Portal das Finanças em vez de linha a linha.")

    if problemas:
        print("\n--- Problemas de leitura " + "-" * 37)
        for p in problemas[:15]:
            print(f"  ! {p}")
        if len(problemas) > 15:
            print(f"  ... e mais {len(problemas) - 15}.")

    print("\n  Os valores da AT prevalecem sobre este resumo.\n")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Agrega exportações CSV do e-Fatura.",
        epilog="Não decide dedutibilidade; os valores da AT prevalecem.",
    )
    p.add_argument("ficheiros", nargs="+", type=Path, help="CSV(s) exportado(s) do e-Fatura")
    p.add_argument("--ano", type=int, help="filtrar por ano de emissão")
    p.add_argument("--json", action="store_true", help="output JSON em vez de resumo")
    p.add_argument("--resumo", action="store_true", help="resumo legível (predefinição)")
    args = p.parse_args(argv)

    registos: list[dict] = []
    problemas: list[str] = []
    for caminho in args.ficheiros:
        if not caminho.exists():
            problemas.append(f"{caminho}: não encontrado")
            continue
        r, pr = le_ficheiro(caminho)
        registos.extend(r)
        problemas.extend(pr)

    if args.ano:
        antes = len(registos)
        registos = [r for r in registos if r["ano"] == args.ano]
        if not registos and antes:
            problemas.append(f"nenhum documento de {args.ano} em {antes} lidos")

    if not registos:
        print("Nenhum documento lido.", file=sys.stderr)
        for pb in problemas:
            print(f"  ! {pb}", file=sys.stderr)
        return 1

    resultado = agrega(registos)
    if args.json:
        print(json.dumps({"resumo": resultado, "problemas": problemas,
                          "documentos": registos}, ensure_ascii=False, indent=2))
    else:
        imprime_resumo(resultado, problemas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
