#!/usr/bin/env python3
"""Testes do parser do e-Fatura e da coerência dos valores de referência.

Correr:  python3 skills/irs-pt/scripts/test_parse_efatura.py
Sem dependências externas. Cria os ficheiros de teste em diretório temporário.
"""
import json, re, subprocess, sys, tempfile, unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent.parent
PARSER = AQUI / "parse_efatura.py"
EXEMPLO = AQUI / "exemplo-efatura.csv"
sys.path.insert(0, str(AQUI))
from parse_efatura import num, norm, ler  # noqa: E402

CAB = "Data Emissão;Nome Emitente;Tipo;Setor;Situação;Valor Total"


def corre(*args):
    r = subprocess.run([sys.executable, str(PARSER), *map(str, args)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def escreve(dir_, nome, texto, enc="utf-8"):
    p = Path(dir_) / nome
    p.write_bytes(texto.encode(enc))
    return p


class TestNumeros(unittest.TestCase):
    def test_formato_pt(self):
        for bruto, esperado in [("1.234,56", 1234.56), ("33,90", 33.90),
                                ("1.016,26", 1016.26), ("450", 450.0)]:
            self.assertAlmostEqual(num(bruto), esperado, places=2, msg=bruto)

    def test_formato_us(self):
        """O separador decimal é o que está mais à direita."""
        self.assertAlmostEqual(num("1,234.56"), 1234.56, places=2)

    def test_degenerados(self):
        for bruto in ("", None, "abc", "€"):
            self.assertEqual(num(bruto), 0.0, msg=repr(bruto))

    def test_simbolo_e_espacos(self):
        self.assertAlmostEqual(num(" 1.250,00 € "), 1250.00, places=2)

    def test_norm_tira_acentos(self):
        self.assertEqual(norm(" Situação "), "situacao")
        self.assertEqual(norm("Data Emissão"), "data emissao")


class TestCodificacao(unittest.TestCase):
    def test_cp1252_nao_rebenta(self):
        """Regressão: o Excel em Windows grava cp1252; antes dava UnicodeDecodeError."""
        with tempfile.TemporaryDirectory() as d:
            f = escreve(d, "cp1252.csv",
                        CAB + "\n05-04-2025;Serviços Atenção Lda;Fatura;Educação;Registada;1.500,00\n",
                        enc="cp1252")
            cod, out, err = corre(f)
            self.assertEqual(cod, 0, err)
            self.assertIn("1500.00", out)
            self.assertIn("Educação", out)

    def test_utf8_bom(self):
        with tempfile.TemporaryDirectory() as d:
            f = escreve(d, "bom.csv", "﻿" + CAB + "\n05-04-2025;A;Fatura;X;Registada;10,00\n")
            cod, out, _ = corre(f)
            self.assertEqual(cod, 0)
            self.assertIn("10.00", out)


class TestEstrutura(unittest.TestCase):
    def test_preambulo_antes_do_cabecalho(self):
        with tempfile.TemporaryDirectory() as d:
            f = escreve(d, "pre.csv",
                        "Exportação e-Fatura\nContribuinte: 999999990\n\n"
                        "Data,Nome Emitente,Tipo,Setor,Estado,Valor Total\n"
                        "01/03/2025,Alfa Lda,Fatura,Saude,Registada,\"1,234.56\"\n"
                        "02/03/2025,Beta Lda,Nota de Credito,Saude,Registada,\"234.56\"\n")
            cod, out, err = corre(f)
            self.assertEqual(cod, 0, err)
            self.assertIn("1000.00", out)  # 1234,56 − 234,56

    def test_newline_dentro_de_aspas(self):
        """Regressão: splitlines() partia campos multilinha entre aspas."""
        with tempfile.TemporaryDirectory() as d:
            f = escreve(d, "aspas.csv", CAB +
                        '\n01-06-2025;"Alfa Lda\nSucursal Porto";Fatura;Saude;Registada;100,00'
                        "\n02-06-2025;Beta;Fatura;Saude;Registada;50,00\n")
            cod, out, err = corre(f)
            self.assertEqual(cod, 0, err)
            self.assertIn("Registos: 2", out)
            self.assertIn("150.00", out)

    def test_colunas_em_falta_falha_com_mensagem(self):
        with tempfile.TemporaryDirectory() as d:
            f = escreve(d, "mau.csv", "Coluna A;Coluna B\nx;y\n")
            cod, _, err = corre(f)
            self.assertEqual(cod, 1)
            self.assertIn("Não encontrei colunas", err)


class TestRegrasDeNegocio(unittest.TestCase):
    def setUp(self):
        cod, out, err = corre(EXEMPLO, "--ano", "2025", "--json")
        self.assertEqual(cod, 0, err)
        self.res = json.loads(out)

    def test_total_do_exemplo(self):
        self.assertAlmostEqual(self.res["total"], 2421.90, places=2)

    def test_nota_de_credito_abate(self):
        """As duas linhas da Telecom (44,00 e −44,00) têm de anular-se."""
        self.assertAlmostEqual(self.res["por_setor"]["Comunicações"]["total"], 0.0, places=2)
        self.assertEqual(self.res["por_setor"]["Comunicações"]["n"], 2)

    def test_anulado_excluido(self):
        """Regressão: 'Anulada' entrava nos totais e inflacionava 25,00 €."""
        self.assertEqual(self.res["anulados"], 1)
        self.assertNotIn("Anulada", self.res["por_estado"])
        self.assertAlmostEqual(self.res["por_setor"]["Outros bens e serviços"]["total"], 65.00, places=2)

    def test_pendentes_incluem_falta_informacao(self):
        """Regressão: só 'Pendente' era detetado; 300 € de 'Falta informação' passavam."""
        estados = {p["estado"] for p in self.res["pendentes"]}
        self.assertEqual(len(self.res["pendentes"]), 2)
        self.assertIn("Falta informação", estados)
        self.assertIn("Pendente", estados)

    def test_filtro_ano(self):
        cod, out, _ = corre(EXEMPLO, "--json")
        todos = json.loads(out)
        self.assertEqual(todos["registos"], 11)          # inclui a linha de 2024
        self.assertEqual(self.res["registos"], 10)       # --ano 2025 descarta-a

    def test_aviso_truncatura(self):
        with tempfile.TemporaryDirectory() as d:
            linhas = [CAB] + [f"{i%28+1:02d}-01-2025;E{i};Fatura;Outros;Registada;10,00" for i in range(305)]
            f = escreve(d, "grande.csv", "\n".join(linhas) + "\n")
            cod, out, _ = corre(f)
            self.assertEqual(cod, 0)
            self.assertIn("AVISO", out)


class TestValoresDeReferencia(unittest.TestCase):
    """A tabela de valores-anuais.md tem de ser internamente coerente."""

    @classmethod
    def setUpClass(cls):
        cls.texto = (RAIZ / "skills/irs-pt/references/valores-anuais.md").read_text(encoding="utf-8")

    def _linha(self, ano):
        m = re.search(rf"^\| {ano} \|(.+)$", self.texto, re.M)
        self.assertIsNotNone(m, f"ano {ano} ausente da tabela")
        return [c.strip() for c in m.group(1).split("|")]

    @staticmethod
    def _eur(celula):
        # aceita "4.462,15 €" e também "~29.748 €" (sem decimais)
        m = re.search(r"([\d.]+?)(?:,(\d{2}))?\s*€", celula)
        assert m, f"sem valor em euros: {celula!r}"
        return float(m.group(1).replace(".", "") + "." + (m.group(2) or "0"))

    def test_deducao_2025_bate_com_a_formula(self):
        ias, ded = self._eur(self._linha(2025)[0]), self._eur(self._linha(2025)[1])
        self.assertAlmostEqual(ded, round(8.54 * ias, 2), places=2)

    def test_limiar_e_deducao_a_dividir_por_015(self):
        for ano in (2025, 2026):  # 2024 tem teste próprio (fórmula diferente)
            ded, limiar = self._eur(self._linha(ano)[1]), self._eur(self._linha(ano)[2])
            self.assertAlmostEqual(limiar, ded / 0.15, delta=1.0, msg=f"ano {ano}")

    def test_2024_usa_a_taxa_de_atualizacao_do_ias(self):
        """2024: 4.104 × 1,06 (taxa de atualização do IAS), não 8,54 × IAS.

        Valor oficial da AT — IRS 2024, deduções, benefícios e taxas.
        """
        ded = self._eur(self._linha(2024)[1])
        self.assertAlmostEqual(ded, 4104 * 1.06, places=2)      # 4.350,24 €
        self.assertNotAlmostEqual(ded, 8.54 * 509.26, delta=0.5)  # 4.349,08 € seria errado

    def test_limiar_2024_coerente_com_a_deducao(self):
        ded, limiar = self._eur(self._linha(2024)[1]), self._eur(self._linha(2024)[2])
        self.assertAlmostEqual(limiar, ded / 0.15, delta=1.0)   # ≈ 29.002 €

    def test_2024_confirmado_na_at(self):
        self.assertIn("confirmado (AT, IRS 2024)", self._linha(2024)[6])
        self.assertIn("IRS_2024", self.texto)

    def test_as_duas_leis_estao_distinguidas(self):
        """A Lei 32/2024 indexou à taxa; o múltiplo 8,54 veio com a Lei 45-A/2024 (OE 2025)."""
        self.assertIn("Lei n.º 32/2024", self.texto)
        self.assertIn("Lei n.º 45-A/2024", self.texto)
        self.assertIn("irs25.aspx", self.texto)

    def test_2026_confirmado_por_fonte_secundaria(self):
        estado = self._linha(2026)[6].lower()
        self.assertIn("fonte secundária", estado)
        self.assertIn("a confirmar", estado)


class TestCoeficientes(unittest.TestCase):
    """Todos os coeficientes do art. 31.º n.º 1 têm de estar na tabela."""

    @classmethod
    def setUpClass(cls):
        cls.texto = (RAIZ / "skills/irs-pt/references/fiscal.md").read_text(encoding="utf-8")

    def test_tabela_cobre_os_seis_coeficientes(self):
        for coef in ("0,15", "0,75", "0,35", "0,95", "0,30", "0,10"):
            self.assertRegex(self.texto, rf"\|\s*{re.escape(coef)}\s*\|", f"falta o coeficiente {coef}")

    def test_subsidios_identificados_pelas_alineas(self):
        self.assertIn("al. e)", self.texto)
        self.assertIn("al. f)", self.texto)

    def test_fonte_dos_coeficientes_presente(self):
        self.assertIn("irs31.aspx", self.texto)


class TestPlugin(unittest.TestCase):
    def test_manifestos_validos(self):
        for f in ("plugin.json", "marketplace.json"):
            dados = json.loads((RAIZ / ".claude-plugin" / f).read_text(encoding="utf-8"))
            self.assertEqual(dados["name"], "irs-pt", f)

    def test_skill_tem_frontmatter(self):
        t = (RAIZ / "skills/irs-pt/SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        self.assertIsNotNone(m, "frontmatter ausente")
        self.assertRegex(m.group(1), r"(?m)^name:\s*irs-pt\s*$")
        self.assertIn("description:", m.group(1))

    def test_referencias_citadas_existem(self):
        t = (RAIZ / "skills/irs-pt/SKILL.md").read_text(encoding="utf-8")
        for ref in set(re.findall(r"`?references/([a-z-]+\.md)", t)):
            self.assertTrue((RAIZ / "skills/irs-pt/references" / ref).exists(), ref)

    def test_gitignore_protege_csv_mas_deixa_o_exemplo(self):
        g = (RAIZ / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("*.csv", g)
        self.assertIn("!skills/irs-pt/scripts/exemplo-efatura.csv", g)


class TestCenarioTresCAEs(unittest.TestCase):
    """O caso real: 3 atividades, coeficientes diferentes, um só limiar.

    Só o rendimento sujeito a 0,75 e 0,35 entra na regra dos 15%; vendas (0,15) não.
    """
    DEDUCAO_2025 = 4462.15

    @staticmethod
    def limiar(servicos_075, servicos_035, deducao, contribuicoes=0.0):
        base = servicos_075 + servicos_035
        automatica = max(deducao, contribuicoes)
        return round(0.15 * base - automatica, 2)

    def test_vendas_nao_entram_na_base(self):
        """20.000 € de vendas não contam: a base é só 10.000 € de serviços."""
        com_vendas = self.limiar(10000, 0, self.DEDUCAO_2025)
        sem_vendas = self.limiar(10000, 0, self.DEDUCAO_2025)
        self.assertEqual(com_vendas, sem_vendas)
        self.assertLess(com_vendas, 0)  # abaixo do limiar: nada a justificar

    def test_abaixo_do_limiar_nada_a_justificar(self):
        """29.747,67 € é o ponto onde 15% do bruto iguala a dedução automática."""
        self.assertLessEqual(self.limiar(29747.67, 0, self.DEDUCAO_2025), 0.01)

    def test_acima_do_limiar_falta_justificar(self):
        """40.000 € em serviços: 6.000 − 4.462,15 = 1.537,85 € por justificar."""
        self.assertAlmostEqual(self.limiar(40000, 0, self.DEDUCAO_2025), 1537.85, places=2)

    def test_tres_caes_somam_so_os_servicos(self):
        """25.000 (0,75) + 10.000 (0,35) + 20.000 vendas → base 35.000."""
        falta = self.limiar(25000, 10000, self.DEDUCAO_2025)
        self.assertAlmostEqual(falta, 0.15 * 35000 - self.DEDUCAO_2025, places=2)
        self.assertAlmostEqual(falta, 787.85, places=2)

    def test_contribuicoes_ss_substituem_a_deducao_quando_maiores(self):
        """21,4% × 70% = 14,98% do bruto — quase os 15% sozinhas."""
        bruto = 60000
        contribuicoes = 0.214 * 0.70 * bruto
        falta = self.limiar(bruto, 0, self.DEDUCAO_2025, contribuicoes)
        self.assertAlmostEqual(falta, 0.15 * bruto - contribuicoes, places=2)
        self.assertAlmostEqual(falta, 12.00, places=2)  # 0,02% de 60.000 €
        self.assertLess(falta, 0.15 * bruto - self.DEDUCAO_2025)


if __name__ == "__main__":
    unittest.main(verbosity=2)
