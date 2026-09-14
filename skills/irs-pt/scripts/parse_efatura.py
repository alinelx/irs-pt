#!/usr/bin/env python3
"""Lê a exportação do e-Fatura ("Obter dados para Excel", CSV) e resume por setor e estado.

Uso:  python parse_efatura.py ficheiro.csv [--ano 2025] [--json]
Só usa a biblioteca padrão. Não envia dados para lado nenhum.
Os nomes das colunas no portal variam; a deteção é por aproximação (ver COLUNAS).
"""
import argparse, csv, json, re, sys
from collections import defaultdict

# candidatos de nome por campo lógico (minúsculas, sem acentos)
COLUNAS = {
    "nif": ["nif emitente", "nif do emitente", "nif"],
    "nome": ["nome emitente", "nome do emitente", "emitente", "nome"],
    "tipo": ["tipo de documento", "tipo documento", "tipo"],
    "data": ["data emissao", "data de emissao", "data"],
    "total": ["valor total", "total", "montante total"],
    "iva": ["iva", "valor iva", "total iva"],
    "estado": ["situacao", "estado", "situacao do documento"],
    "setor": ["setor de atividade", "setor", "atividade", "sector"],
}
TIPOS_NEGATIVOS = ("nota de credito", "nc", "nota de crédito")

def norm(s):
    s = s.strip().lower()
    s = re.sub(r"[áàãâ]", "a", s); s = re.sub(r"[éê]", "e", s); s = re.sub(r"[íï]", "i", s)
    s = re.sub(r"[óõô]", "o", s); s = re.sub(r"[úü]", "u", s); s = s.replace("ç", "c")
    return re.sub(r"\s+", " ", s)

def mapear(cabecalho):
    n = {norm(c): c for c in cabecalho}
    out = {}
    for campo, cands in COLUNAS.items():
        for c in cands:
            hit = next((orig for k, orig in n.items() if k == c or k.startswith(c)), None)
            if hit:
                out[campo] = hit; break
    return out

def num(v):
    if v is None: return 0.0
    v = str(v).strip().replace("€", "").replace(" ", "")
    if "," in v and "." in v: v = v.replace(".", "").replace(",", ".")
    elif "," in v: v = v.replace(",", ".")
    try: return float(v)
    except ValueError: return 0.0

def ler(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        amostra = f.read(4096); f.seek(0)
        try: dialecto = csv.Sniffer().sniff(amostra, delimiters=";,\t")
        except csv.Error: dialecto = csv.excel; dialecto.delimiter = ";"
        return list(csv.DictReader(f, dialect=dialecto))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ficheiro"); ap.add_argument("--ano", type=int); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    linhas = ler(a.ficheiro)
    if not linhas: sys.exit("CSV vazio ou ilegível.")
    m = mapear(linhas[0].keys())
    faltam = [c for c in ("total", "data") if c not in m]
    if faltam: sys.exit(f"Não encontrei colunas {faltam}. Cabeçalho: {list(linhas[0].keys())}")

    por_setor, por_estado, docs = defaultdict(lambda: [0, 0.0]), defaultdict(lambda: [0, 0.0]), []
    for r in linhas:
        data = r.get(m["data"], "")
        if a.ano and str(a.ano) not in data: continue
        total = num(r.get(m["total"]))
        tipo = norm(r.get(m.get("tipo", ""), "") or "")
        if any(t in tipo for t in TIPOS_NEGATIVOS) and total > 0: total = -total
        setor = (r.get(m.get("setor", ""), "") or "sem setor").strip()
        estado = (r.get(m.get("estado", ""), "") or "?").strip()
        por_setor[setor][0] += 1; por_setor[setor][1] += total
        por_estado[estado][0] += 1; por_estado[estado][1] += total
        docs.append({"data": data, "emitente": r.get(m.get("nome", ""), ""), "nif": r.get(m.get("nif", ""), ""),
                     "tipo": tipo, "setor": setor, "estado": estado, "total": round(total, 2)})

    docs.sort(key=lambda d: d["data"])
    res = {"registos": len(docs), "total": round(sum(d["total"] for d in docs), 2),
           "por_setor": {k: {"n": v[0], "total": round(v[1], 2)} for k, v in sorted(por_setor.items(), key=lambda kv: -kv[1][1])},
           "por_estado": {k: {"n": v[0], "total": round(v[1], 2)} for k, v in por_estado.items()},
           "pendentes": [d for d in docs if "pend" in norm(d["estado"])],
           "aviso_limite": len(linhas) >= 300}
    if a.json: print(json.dumps(res, ensure_ascii=False, indent=2)); return
    print(f"Registos: {res['registos']}  |  Total: {res['total']:.2f} €")
    if res["aviso_limite"]: print("AVISO: ≥300 linhas — a exportação pode estar truncada; exporta por período mais curto.")
    print("\nPor setor:")
    for k, v in res["por_setor"].items(): print(f"  {k:<40} {v['n']:>4}  {v['total']:>10.2f} €")
    print("\nPor estado:")
    for k, v in res["por_estado"].items(): print(f"  {k:<40} {v['n']:>4}  {v['total']:>10.2f} €")
    print(f"\nPendentes de classificação: {len(res['pendentes'])}")
    for d in res["pendentes"][:20]: print(f"  {d['data']}  {d['emitente'][:30]:<30} {d['total']:>9.2f} €  [{d['setor']}]")

if __name__ == "__main__":
    main()
