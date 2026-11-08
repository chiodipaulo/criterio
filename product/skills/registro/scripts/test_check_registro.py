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


def expect(label, text, needle, example=False):
    errors = check_registro.check_text(text, example=example)
    hit = any(needle in error for error in errors)
    print(("ok   " if hit else "FAIL ") + label + ("" if hit else (": expected %r in %s" % (needle, errors))))
    return 0 if hit else 1


def expect_ok(label, text, example=False):
    errors = check_registro.check_text(text, example=example)
    print(("ok   " if not errors else "FAIL ") + label + ("" if not errors else (": " + " | ".join(errors))))
    return 0 if not errors else 1


def main():
    failures = 0
    failures += expect_ok("fato mínimo passa", block("fato", "texto: Um preço publicado.\nautoriza_execucao: não\n", ident="E1"))
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
        block("hipotese", "status: não testada\napoio: nenhum\nautoriza_execucao: não\nvalor: R$ 49,00 por mês\n", ident="H1"),
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

    example = os.path.join(os.path.dirname(__file__), "..", "references", "exemplo-escala-miuda.md")
    if not os.path.isfile(example):
        print("FAIL exemplo ausente: " + example)
        failures += 1
    else:
        text = open(example, encoding="utf-8").read()
        failures += expect_ok("exemplo completo passa", text, example=True)

    print("%s failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
