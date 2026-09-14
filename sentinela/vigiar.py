#!/usr/bin/env python3
"""Sentinela: vigia páginas oficiais e escreve um alerta quando o texto muda.

Uso:  python sentinela/vigiar.py            # compara e atualiza snapshots
      python sentinela/vigiar.py --init     # só cria snapshots, sem alerta
Saída: sentinela/snapshots/<id>.txt (texto extraído) e sentinela/ALERTA.md (se houver mudanças ou falhas).
Só stdlib. Não decide nada: reporta. A atualização da skill continua a ser humana.
"""
import argparse, difflib, hashlib, json, re, sys, urllib.request, urllib.error
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

AQUI = Path(__file__).parent
SNAP = AQUI / "snapshots"
UA = "Mozilla/5.0 (compatible; irs-pt-sentinela/0.1; +https://github.com/alinelx/irs-pt)"
IGNORAR = ("script", "style", "noscript", "header", "footer", "nav", "svg")

class Texto(HTMLParser):
    def __init__(self):
        super().__init__(); self.p = []; self.saltar = 0
    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR: self.saltar += 1
    def handle_endtag(self, tag):
        if tag in IGNORAR and self.saltar: self.saltar -= 1
    def handle_data(self, d):
        if not self.saltar and d.strip(): self.p.append(d.strip())

def extrair(html):
    t = Texto(); t.feed(html)
    txt = "\n".join(t.p)
    txt = re.sub(r"\d{1,2}[-/]\d{1,2}[-/]\d{4}\s*\d{1,2}:\d{2}(:\d{2})?", "<data-hora>", txt)  # timestamps dinâmicos
    return re.sub(r"\n{2,}", "\n", txt).strip()

def buscar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-PT,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try: return raw.decode(enc)
        except UnicodeDecodeError: continue
    return raw.decode("utf-8", "replace")

def obter(f):
    """Tenta a URL principal e as alternativas. Devolve (texto, url_usada) ou levanta a última falha.

    O marcador é texto que TEM de aparecer na página. Uma página que responde 200 mas só
    traz o aviso de cookies não passa — foi assim que a Segurança Social escapou à guarda
    do tamanho mínimo na primeira execução.
    """
    marcador = (f.get("marcador") or "").lower()
    erros = []
    for url in [f["url"], *f.get("alternativas", [])]:
        try:
            txt = extrair(buscar(url))
        except Exception as e:
            erros.append(f"{url} -> {type(e).__name__}: {e}"); continue
        if len(txt) < 200:
            erros.append(f"{url} -> quase vazia ({len(txt)} chars)"); continue
        if marcador and marcador not in txt.lower():
            erros.append(f"{url} -> sem o marcador {marcador!r} ({len(txt)} chars) — página errada ou só chrome")
            continue
        return txt, url
    raise LookupError(" | ".join(erros))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--init", action="store_true"); a = ap.parse_args()
    fontes = json.loads((AQUI / "fontes.json").read_text(encoding="utf-8"))["fontes"]
    SNAP.mkdir(exist_ok=True)
    mudancas, falhas, novas = [], [], []
    for f in fontes:
        fid = f["id"]
        try:
            novo, usada = obter(f)
        except LookupError as e:
            falhas.append((f, str(e))); continue
        if usada != f["url"]:
            print(f"  NOTA {fid}: a URL principal falhou; funcionou a alternativa {usada}")
        p = SNAP / f"{fid}.txt"
        if not p.exists():
            p.write_text(novo, encoding="utf-8"); novas.append(f); continue
        antigo = p.read_text(encoding="utf-8")
        if hashlib.sha256(antigo.encode()).hexdigest() != hashlib.sha256(novo.encode()).hexdigest():
            diff = "\n".join(difflib.unified_diff(antigo.splitlines(), novo.splitlines(), "antes", "depois", lineterm="", n=2))
            mudancas.append((f, diff)); p.write_text(novo, encoding="utf-8")

    if a.init or not (mudancas or falhas):
        print(f"ok — {len(fontes)} fontes, {len(novas)} novas, sem mudanças" if not falhas else f"init com {len(falhas)} falhas")
        for f, e in falhas: print(f"  FALHA {f['id']}: {e}")
        (AQUI / "ALERTA.md").unlink(missing_ok=True); return

    linhas = [f"# Sentinela — {date.today().isoformat()}", ""]
    if mudancas:
        linhas.append(f"## {len(mudancas)} fonte(s) com texto alterado\n")
        for f, diff in mudancas:
            linhas += [f"### {f['id']}", f"- URL: {f['url']}", f"- Porque interessa: {f['porque']}", "",
                       "```diff", diff[:6000] + ("\n... (diff truncado)" if len(diff) > 6000 else ""), "```", ""]
        linhas += ["**Ação humana:** ler o diff, decidir se afeta `skills/irs-pt/references/*.md`, atualizar e correr os testes. "
                   "A sentinela não altera a skill.", ""]
    if falhas:
        linhas.append(f"## {len(falhas)} fonte(s) inacessíveis ou sem o marcador esperado\n")
        for f, e in falhas: linhas.append(f"- `{f['id']}` — {f['url']} — {e}")
        linhas += ["", "Se persistir, a URL mudou ou o site passou a bloquear: atualizar `sentinela/fontes.json`.", ""]
    (AQUI / "ALERTA.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"ALERTA: {len(mudancas)} mudanças, {len(falhas)} falhas"); sys.exit(0)

if __name__ == "__main__":
    main()
