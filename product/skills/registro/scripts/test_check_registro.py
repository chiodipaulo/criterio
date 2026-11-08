#!/usr/bin/env python3
"""Failing cases for check_registro.py. Run from anywhere:

    python <skill dir>/scripts/test_check_registro.py
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_registro  # noqa: E402

BASE = """```registro
id: {id}
tipo: {tipo}
autor: Marina Alves (FICTÍCIO)
motivo: {motivo}
fonte: HIPOTÉTICO
data: 08/11/2026
fuso: America/Sao_Paulo
{extra}```
"""


def block(tipo, extra, motivo="mostrar o formato", ident=None):
    return BASE.format(id=ident or "R1", tipo=tipo, motivo=motivo, extra=extra)


def expect(label, text, needle, example=False, base_dir=None):
    errors = check_registro.check_text(text, example=example, base_dir=base_dir)
    hit = any(needle in error for error in errors)
    print(("ok   " if hit else "FAIL ") + label + ("" if hit else (": expected %r in %s" % (needle, errors))))
    return 0 if hit else 1


def expect_ok(label, text, example=False, base_dir=None):
    errors = check_registro.check_text(text, example=example, base_dir=base_dir)
    print(("ok   " if not errors else "FAIL ") + label + ("" if not errors else (": " + " | ".join(errors))))
    return 0 if not errors else 1


PR_FLAGS = (
    "autoriza_versao_exclusiva: não\n"
    "autoriza_violar_restricao: não\n"
    "autoriza_construir: não\n"
    "autoriza_pesquisar: não\n"
    "texto: Pedido de troca aceito pela outra pessoa.\n"
)


def prioridade(ident, nota, anterior, extra=""):
    return block(
        "prioridade",
        "item: Pedido de troca\nnota: %s\nescala: 1-5\nnota_anterior: %s\n%s%s"
        % (nota, anterior, PR_FLAGS, extra),
        ident=ident,
    )


def com_data(text, data):
    return text.replace("data: 08/11/2026", "data: " + data, 1)


def main():
    failures = 0
    failures += expect_ok(
        "fato mínimo passa",
        block("fato", "texto: Um preço publicado.\nautoriza_execucao: não\n", ident="E1").replace(
            "fonte: HIPOTÉTICO", "fonte: https://exemplo.invalid/preco"),
    )
    failures += expect(
        "fato não autoriza execução",
        block("fato", "texto: Um preço publicado.\nautoriza_execucao: sim\n", ident="E1"),
        "autoriza_execucao tem de ser não",
    )
    failures += expect(
        "data ISO é recusada",
        block("fato", "texto: Um preço.\nautoriza_execucao: não\n", ident="E1").replace("08/11/2026", "2026-11-08"),
        "dd/mm/aaaa",
    )
    failures += expect(
        "valor sem reais é recusado",
        block("hipotese", "status: não testada\napoio: nenhum\nautoriza_execucao: não\nvalor: 49 por mês\n", ident="H1"),
        "não está em reais",
    )
    failures += expect_ok(
        "valor em reais passa",
        block(
            "hipotese",
            "status: não testada\napoio: nenhum\nautoriza_execucao: não\n"
            "valor: R$ 49,00 por mês\ntexto: Coordenadoras pagariam esse valor por mês.\n",
            ident="H1",
        ),
    )
    failures += expect(
        "restrição sem autoridade é recusada",
        block("restricao", "texto: Sem versão exclusiva.\npode_violar: não\n"),
        "falta autoridade_pra_mudar",
    )
    failures += expect(
        "restrição não pode ser marcada como violável",
        block("restricao", "texto: Sem versão exclusiva.\nautoridade_pra_mudar: a dona do produto\npode_violar: sim\n"),
        "pode_violar tem de ser não",
    )
    failures += expect(
        "cliente não autoriza versão exclusiva",
        block(
            "preferencia",
            "texto: Quer uma versão só dela.\nde_quem: cliente\n"
            "autoriza_execucao: não\nautoriza_versao_exclusiva: sim\n"
            "autoriza_violar_restricao: não\nautoriza_construir: não\n",
            ident="P1",
        ),
        "autoriza_versao_exclusiva tem de ser não",
    )
    failures += expect(
        "nota de prioridade não autoriza construir",
        block(
            "prioridade",
            "item: Troca de plantão\nnota: 4\nescala: 1-5\nnota_anterior: 2\n"
            "autoriza_versao_exclusiva: não\nautoriza_violar_restricao: não\n"
            "autoriza_construir: sim\nautoriza_pesquisar: não\n",
            ident="PR1",
        ),
        "autoriza_construir tem de ser não",
    )
    failures += expect(
        "escala ausente no nome é recusada",
        block(
            "prioridade",
            "item: Troca de plantão\nnota: 4\nescala: 0-100\nnota_anterior: 2\n"
            "autoriza_versao_exclusiva: não\nautoriza_violar_restricao: não\n"
            "autoriza_construir: não\nautoriza_pesquisar: não\n",
            ident="PR1",
        ),
        "escala",
    )
    failures += expect(
        "permissão não executa",
        block(
            "permissao",
            "acao: construir\nescopo: a primeira versão\nautorizado_por: ninguém\n"
            "executa: sim\nversao_exclusiva: não\nsituacao: recusada\n",
            ident="PE1",
        ),
        "executa tem de ser não",
    )
    old = block("restricao", "texto: Sem versão exclusiva.\nautoridade_pra_mudar: a dona do produto\npode_violar: não\n")
    bad_change = block(
        "restricao",
        "texto: Agora pode ter versão exclusiva.\nautoridade_pra_mudar: a dona do produto\n"
        "pode_violar: não\nsubstitui: R1\nautoridade_citada: o cliente grande\n",
        ident="R2",
    )
    failures += expect("quem não tem autoridade não muda a restrição", old + "\n" + bad_change, "autoridade_citada")
    good_change = block(
        "restricao",
        "texto: Texto novo, mesma barra.\nautoridade_pra_mudar: a dona do produto\n"
        "pode_violar: não\nsubstitui: R1\nautoridade_citada: a dona do produto\n",
        ident="R2",
    )
    failures += expect_ok("a autoridade nomeada pode registrar a troca", old + "\n" + good_change)
    same = block(
        "permissao",
        "acao: pesquisar\nescopo: ler páginas públicas\nautorizado_por: Marina Alves (FICTÍCIO)\n"
        "executa: não\nversao_exclusiva: não\nsituacao: concedida\n",
        ident="PE1",
    )
    decision = block(
        "decisao",
        "pesquisar_id: PE1\nconstruir_id: PE1\nexecuta: não\n",
        ident="D1",
    )
    failures += expect("uma permissão não cobre pesquisar e construir", same + "\n" + decision, "mesma permissão")

    inicio = com_data(prioridade("PR0", "2", "nenhuma"), "03/11/2026")
    seguinte = prioridade("PR1", "4", "2", "anterior_id: PR0\n")
    failures += expect_ok("cadeia de prioridade com o registro inicial", inicio + "\n" + seguinte)
    mesmo_dia = prioridade("PR1", "4", "2", "anterior_id: PR0\n")
    failures += expect_ok("cadeia legítima no mesmo dia", inicio.replace("03/11/2026", "08/11/2026") + "\n" + mesmo_dia)
    meio = com_data(prioridade("PR1", "3", "2", "anterior_id: PR0\n"), "03/11/2026")
    fim = prioridade("PR2", "4", "3", "anterior_id: PR1\n")
    failures += expect_ok("cadeia legítima de três registros", com_data(prioridade("PR0", "2", "nenhuma"), "01/11/2026") + "\n" + meio + "\n" + fim)
    auto = prioridade("PR1", "4", "4", "anterior_id: PR1\n")
    failures += expect("autociclo de prioridade", auto, "ciclo")
    ciclo_a = prioridade("PA", "4", "3", "anterior_id: PB\n")
    ciclo_b = prioridade("PB", "3", "4", "anterior_id: PA\n")
    failures += expect("ciclo de dois na mesma data", ciclo_a + "\n" + ciclo_b, "ciclo")
    ciclo_1 = prioridade("P1", "4", "2", "anterior_id: P3\n")
    ciclo_3 = prioridade("P3", "2", "3", "anterior_id: P2\n")
    ciclo_2 = prioridade("P2", "3", "4", "anterior_id: P1\n")
    failures += expect("ciclo de três", ciclo_1 + "\n" + ciclo_3 + "\n" + ciclo_2, "ciclo")
    solto = prioridade("PR0", "2", "5")
    filho = prioridade("PR1", "4", "2", "anterior_id: PR0\n")
    failures += expect("cadeia sem início válido", solto + "\n" + filho, "não termina")
    failures += expect("nota 4 sem o registro da nota 2", prioridade("PR1", "4", "2"), "registro anterior")
    failures += expect("nota nenhuma não é uma nota", prioridade("PR9", "nenhuma", "nenhuma"), "nota")
    errada = prioridade("PR1", "4", "3", "anterior_id: PR0\n")
    failures += expect("nota anterior não bate com o registro ligado", inicio + "\n" + errada, "não é a nota")
    outro_item = prioridade("PR1", "4", "2", "anterior_id: PR0\n").replace(
        "item: Pedido de troca", "item: Outro item", 1)
    failures += expect("cadeia com item diferente", inicio + "\n" + outro_item, "item")
    cedo = com_data(prioridade("PR1", "4", "2", "anterior_id: PR0\n"), "01/11/2026")
    failures += expect("data da nota nova antes da nota ligada", inicio + "\n" + cedo, "ordem")
    dois = com_data(prioridade("PR8", "1", "nenhuma"), "02/11/2026")
    failures += expect("dois inícios pro mesmo item", inicio + "\n" + dois, "início")

    failures += expect(
        "registro sem texto",
        block("fato", "autoriza_execucao: não\nfonte: https://exemplo.invalid/preco\n", ident="E9").replace(
            "fonte: HIPOTÉTICO\n", ""),
        "texto",
    )
    failures += expect(
        "fuso que não é IANA",
        block("fato", "texto: Um preço publicado na página.\nautoriza_execucao: não\n", ident="E8").replace(
            "America/Sao_Paulo", "Brasil"),
        "fuso",
    )
    failures += expect(
        "fato sem fonte rastreável",
        block("fato", "texto: Um preço publicado na página.\nautoriza_execucao: não\n", ident="E7"),
        "fonte",
    )
    failures += expect_ok(
        "fato com URL rastreável",
        block("fato", "texto: Um preço publicado na página.\nautoriza_execucao: não\n", ident="E6").replace(
            "fonte: HIPOTÉTICO", "fonte: https://exemplo.invalid/preco"),
    )
    import tempfile
    tmp = tempfile.mkdtemp()
    open(os.path.join(tmp, "preco.md"), "w", encoding="utf-8").write("FICTÍCIO R$ 89,00\n")
    local_ok = block(
        "fato", "texto: Um preço publicado na página.\nautoriza_execucao: não\n", ident="E5",
    ).replace("fonte: HIPOTÉTICO", "fonte: local: preco.md")
    failures += expect_ok("fato com arquivo local", local_ok, base_dir=tmp)
    local_bad = local_ok.replace("fonte: local: preco.md", "fonte: local: nao-existe.md")
    failures += expect("fato com arquivo local ausente", local_bad, "fonte", base_dir=tmp)
    escapa = local_ok.replace("fonte: local: preco.md", "fonte: local: ../preco.md")
    failures += expect("fonte local não sai da pasta", escapa, "fonte", base_dir=tmp)

    if not hasattr(check_registro, "render_html"):
        print("FAIL render_html ausente")
        failures += 1
    else:
        amostra = block(
            "fato", "texto: Um preço publicado na página.\nautoriza_execucao: não\n", ident="E4",
        ).replace("fonte: HIPOTÉTICO", "fonte: https://exemplo.invalid/preco")
        md_records, md_errors = check_registro.parse_blocks(amostra)
        failures += expect_ok("amostra markdown pra round-trip", amostra)
        html = check_registro.render_html(md_records)
        html_records, html_errors = check_registro.parse_blocks(html)
        same_records = check_registro.same_records(md_records, html_records)
        if md_errors or html_errors or not same_records:
            print("FAIL round-trip HTML: md=%s html=%s iguais=%s" % (md_errors, html_errors, same_records))
            failures += 1
        else:
            print("ok   round-trip markdown e HTML")
        de_novo, de_novo_erros = check_registro.parse_blocks(check_registro.render_markdown(html_records))
        if de_novo_erros or not check_registro.same_records(md_records, de_novo):
            print("FAIL round-trip de volta ao markdown")
            failures += 1
        else:
            print("ok   HTML volta ao markdown equivalente")
        duplicado = amostra + "\n" + html
        failures += expect("markdown e HTML no mesmo arquivo", duplicado, "duas representações")

    def html_de(pairs):
        rows = "\n".join("<dt>%s</dt><dd>%s</dd>" % pair for pair in pairs)
        return "<article class=\"registro\">\n<dl>\n%s\n</dl>\n</article>" % rows

    def md_com_chave_repetida(text, key, value):
        return text.replace("\n```", "\n%s: %s\n```" % (key, value), 1)

    fato_base = [
        ("id", "E1"), ("tipo", "fato"), ("autor", "Marina Alves (FICTÍCIO)"),
        ("motivo", "mostrar o formato"), ("fonte", "https://exemplo.invalid/preco"),
        ("data", "08/11/2026"), ("fuso", "America/Sao_Paulo"),
        ("texto", "Um preço publicado na página."), ("autoriza_execucao", "não"),
    ]
    nota_base = [
        ("id", "PR0"), ("tipo", "prioridade"), ("autor", "Marina Alves (FICTÍCIO)"),
        ("motivo", "mostrar o formato"), ("fonte", "HIPOTÉTICO"),
        ("data", "08/11/2026"), ("fuso", "America/Sao_Paulo"),
        ("texto", "Pedido de troca aceito pela outra pessoa."),
        ("item", "Pedido de troca"), ("nota", "2"), ("escala", "1-5"),
        ("nota_anterior", "nenhuma"), ("autoriza_versao_exclusiva", "não"),
        ("autoriza_violar_restricao", "não"), ("autoriza_construir", "não"),
        ("autoriza_pesquisar", "não"),
    ]
    perm_base = [
        ("id", "PE1"), ("tipo", "permissao"), ("autor", "Marina Alves (FICTÍCIO)"),
        ("motivo", "mostrar o formato"), ("fonte", "HIPOTÉTICO"),
        ("data", "08/11/2026"), ("fuso", "America/Sao_Paulo"),
        ("texto", "Permissão de construir ainda sem executar."),
        ("acao", "construir"), ("escopo", "Nenhum escopo nesta prova."),
        ("autorizado_por", "ninguém"), ("executa", "sim"), ("versao_exclusiva", "não"),
        ("situacao", "recusada"),
    ]
    repetidos = (
        ("id", fato_base, "E9"),
        ("nota", nota_base, "5"),
        ("executa", perm_base, "não"),
        ("texto", fato_base, "Outro texto longo o bastante."),
        ("fonte", fato_base, "https://exemplo.invalid/outra"),
    )
    for key, base, extra in repetidos:
        md = check_registro.render_markdown([{k: v for k, v in base}])
        md = md_com_chave_repetida(md, key, extra)
        html_dup = html_de(base + [(key, extra)])
        failures += expect("markdown recusa %s repetido" % key, md, "campo repetido")
        failures += expect("HTML recusa %s repetido" % key, html_dup, "campo repetido")

    frase = check_registro.COMPARACAO_DE_TEXTO_NAO_AUTENTICA
    for rel in ("../SKILL.md", "../references/modelo.md"):
        corpo = open(os.path.join(os.path.dirname(__file__), rel), encoding="utf-8").read()
        if frase not in corpo:
            print("FAIL documentação sem o limite da comparação de texto: " + rel)
            failures += 1
        else:
            print("ok   limite da comparação de texto em " + rel)
    caixa = block(
        "restricao",
        "texto: Texto novo, mesma barra.\nautoridade_pra_mudar: a dona do produto\n"
        "pode_violar: não\nsubstitui: R1\nautoridade_citada: A dona do produto\n",
        ident="R2",
    )
    failures += expect("maiúscula diferente não é a autoridade", old + "\n" + caixa, "autoridade_citada")

    example = os.path.join(os.path.dirname(__file__), "..", "references", "exemplo-escala-miuda.md")
    if not os.path.isfile(example):
        print("FAIL exemplo ausente: " + example)
        failures += 1
    else:
        text = open(example, encoding="utf-8").read()
        failures += expect_ok(
            "exemplo completo passa", text, example=True,
            base_dir=os.path.dirname(example),
        )

    print("%s failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
