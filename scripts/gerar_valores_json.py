#!/usr/bin/env python3
"""Gera valores-anuais.json a partir de valores-anuais.md.

O markdown é a fonte de verdade — editável por humanos, com as notas e as fontes.
O JSON é o que a app mobile lê. Este script deriva um do outro; nunca o contrário.

Uso:
    python3 scripts/gerar_valores_json.py            # (re)escreve o JSON
    python3 scripts/gerar_valores_json.py --check    # exit 1 se divergirem
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MD = RAIZ / "skills/irs-pt/references/valores-anuais.md"
JSON = RAIZ / "skills/irs-pt/references/valores-anuais.json"

# Ordem das colunas da tabela de anos, a seguir ao ano.
COLUNAS = (
    "ias",
    "deducao_especifica",
    "limiar_justificacao",
    "iva_art53_limite",
    "iva_saida_imediata",
    "ss_isencao_acumulacao_mensal",
)
LINHA_ANO = re.compile(r"^\|\s*(\d{4})\s*\|(.+)\|\s*$", re.M)


def eur(celula: str) -> float | None:
    """Lê o primeiro valor em euros da célula. Aceita '4.462,15 €' e '~29.748 €'."""
    m = re.search(r"([\d.]+?)(?:,(\d{1,2}))?\s*€", celula)
    if not m:
        return None
    return float(m.group(1).replace(".", "") + "." + (m.group(2) or "0"))


def extrair(md: str) -> dict:
    anos: dict[str, dict] = {}
    for m in LINHA_ANO.finditer(md):
        ano, resto = m.group(1), m.group(2)
        celulas = [c.strip() for c in resto.split("|")]
        if len(celulas) < len(COLUNAS) + 1:
            continue  # não é a tabela de anos
        registo = {campo: eur(celulas[i]) for i, campo in enumerate(COLUNAS)}
        estado = celulas[len(COLUNAS)]
        estado_limpo = re.sub(r"[*`]", "", estado).strip()
        registo["estado"] = estado_limpo
        # "confirmado" é o prefixo; "a confirmar" em qualquer sítio é uma reserva por resolver
        registo["confirmado"] = estado_limpo.lower().startswith("confirmado")
        registo["reservas"] = "a confirmar" in estado_limpo.lower()
        anos[ano] = registo

    estruturais = {
        "coeficiente_regra_15pct": 0.15,
        "afetacao_parcial": 0.25,
        "regime_simplificado_limite": eur("200.000 €") if "200.000" in md else 200000.0,
        "ss_taxa_independente": 0.214,        # prestação de serviços / profissionais livres
        "ss_taxa_eni_comercial": 0.252,       # ENI comercial e industrial, titulares de EIRL
        "ss_base_servicos": 0.70,
        "ss_base_vendas": 0.20,
    }
    return {
        "_gerado_por": "scripts/gerar_valores_json.py",
        "_fonte": "skills/irs-pt/references/valores-anuais.md",
        "_aviso": "Ficheiro derivado. Não editar à mão — editar o markdown e regerar.",
        "schema": 1,
        "anos": anos,
        "estruturais": estruturais,
    }


def serializar(dados: dict) -> str:
    return json.dumps(dados, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gera valores-anuais.json a partir do markdown.")
    ap.add_argument("--check", action="store_true", help="não escreve; falha se o JSON estiver dessincronizado")
    args = ap.parse_args(argv)

    if not MD.exists():
        print(f"markdown não encontrado: {MD}", file=sys.stderr)
        return 1

    esperado = serializar(extrair(MD.read_text(encoding="utf-8")))

    if args.check:
        if not JSON.exists():
            print(f"{JSON.relative_to(RAIZ)} não existe. Correr sem --check para o gerar.", file=sys.stderr)
            return 1
        atual = JSON.read_text(encoding="utf-8")
        if atual != esperado:
            print(f"{JSON.relative_to(RAIZ)} está dessincronizado de "
                  f"{MD.relative_to(RAIZ)}. Correr sem --check para regerar.", file=sys.stderr)
            return 1
        print("JSON sincronizado com o markdown.")
        return 0

    JSON.write_text(esperado, encoding="utf-8")
    dados = json.loads(esperado)
    print(f"escrito {JSON.relative_to(RAIZ)} — {len(dados['anos'])} anos: "
          + ", ".join(f"{a} ({'confirmado' if v['confirmado'] else 'por confirmar'})"
                      for a, v in sorted(dados["anos"].items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
