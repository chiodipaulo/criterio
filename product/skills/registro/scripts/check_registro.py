#!/usr/bin/env python3
"""check_registro.py — structural checks for a Critério registro file.

The fences are portable text. This script does not call a model and does not
decide that a claim is true. It checks that each record has the fields the
skill requires, that a priority score keeps its previous value, and that no
record grants itself the right to execute.

    python <skill dir>/scripts/check_registro.py <file>
    python <skill dir>/scripts/check_registro.py --example <file>
"""
import datetime
import re
import sys

TYPES = {
    "fato", "hipotese", "preferencia", "restricao", "objetivo",
    "prioridade", "permissao", "decisao", "meta",
}
COMMON = {"id", "tipo", "autor", "motivo", "fonte", "data", "fuso", "texto"}
EXTRA = {
    "fato": {"autoriza_execucao"},
    "hipotese": {"status", "apoio", "valor", "autoriza_execucao"},
    "preferencia": {
        "de_quem", "autoriza_execucao", "autoriza_versao_exclusiva",
        "autoriza_violar_restricao", "autoriza_construir",
    },
    "restricao": {"autoridade_pra_mudar", "pode_violar", "substitui", "autoridade_citada"},
    "objetivo": {"autoriza_execucao"},
    "prioridade": {
        "item", "nota", "escala", "nota_anterior", "autoriza_versao_exclusiva",
        "autoriza_violar_restricao", "autoriza_construir", "autoriza_pesquisar", "cita",
    },
    "permissao": {"acao", "escopo", "autorizado_por", "executa", "versao_exclusiva", "situacao"},
    "decisao": {"pesquisar_id", "construir_id", "executa"},
    "meta": {"completo", "rotulo"},
}
REQUIRED = {
    "fato": ["autoriza_execucao"],
    "hipotese": ["status", "apoio", "autoriza_execucao"],
    "preferencia": [
        "de_quem", "autoriza_execucao", "autoriza_versao_exclusiva",
        "autoriza_violar_restricao", "autoriza_construir",
    ],
    "restricao": ["autoridade_pra_mudar", "pode_violar"],
    "objetivo": ["autoriza_execucao"],
    "prioridade": [
        "item", "nota", "escala", "nota_anterior", "autoriza_versao_exclusiva",
        "autoriza_violar_restricao", "autoriza_construir", "autoriza_pesquisar",
    ],
    "permissao": ["acao", "escopo", "autorizado_por", "executa", "versao_exclusiva", "situacao"],
    "decisao": ["pesquisar_id", "construir_id", "executa"],
    "meta": ["completo", "rotulo"],
}
MUST_BE_NAO = {
    "autoriza_execucao", "autoriza_versao_exclusiva", "autoriza_violar_restricao",
    "autoriza_construir", "autoriza_pesquisar", "pode_violar", "executa", "versao_exclusiva",
}
STATUS = {"não testada", "apoiada", "enfraquecida", "refutada"}
FENCE = re.compile(r"```registro\n(.*?)```", re.DOTALL)
VALOR = re.compile(r"^R\$ \d{1,3}(?:\.\d{3})*,\d{2}(?: .+)?$")
EXECUTION_LINE = "Este arquivo não é ordem de executar."


def valid_date(value):
    match = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", value or "")
    if not match:
        return False
    day, month, year = (int(match.group(i)) for i in (1, 2, 3))
    try:
        datetime.date(year, month, day)
    except ValueError:
        return False
    return True


def parse_blocks(text):
    """Return (records, errors). A record is a dict of string fields plus _id label."""
    records, errors = [], []
    for index, body in enumerate(FENCE.findall(text), 1):
        rec, seen = {}, set()
        for line_no, line in enumerate(body.splitlines(), 1):
            if not line.strip():
                continue
            if ":" not in line:
                errors.append("bloco %s linha %s: campo sem dois-pontos" % (index, line_no))
                continue
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            if not re.fullmatch(r"[a-z_]+", key):
                errors.append("bloco %s: campo desconhecido %r" % (index, key))
                continue
            if key in seen:
                errors.append("bloco %s: campo repetido %s" % (index, key))
            seen.add(key)
            rec[key] = value
        rec["_bloco"] = str(index)
        records.append(rec)
    return records, errors


def _need(errors, rec, key):
    if not rec.get(key):
        errors.append("%s: falta %s" % (rec.get("id") or ("bloco " + rec["_bloco"]), key))
        return False
    return True


def validate_records(records):
    errors, by_id = [], {}
    for rec in records:
        label = rec.get("id") or ("bloco " + rec.get("_bloco", "?"))
        for key in ("id", "tipo", "autor", "motivo", "fonte", "data", "fuso"):
            _need(errors, rec, key)
        tipo = rec.get("tipo", "")
        if tipo and tipo not in TYPES:
            errors.append("%s: tipo %r fora da lista" % (label, tipo))
            continue
        if rec.get("id"):
            if not re.fullmatch(r"[A-Z][A-Z0-9]*", rec["id"]):
                errors.append("%s: id fora do formato" % label)
            elif rec["id"] in by_id:
                errors.append("%s: id repetido" % label)
            else:
                by_id[rec["id"]] = rec
        if rec.get("data") and not valid_date(rec["data"]):
            errors.append("%s: data %r não está em dd/mm/aaaa" % (label, rec["data"]))
        if tipo:
            allowed = COMMON | EXTRA[tipo]
            for key in rec:
                if key.startswith("_"):
                    continue
                if key not in allowed:
                    errors.append("%s: campo %s não cabe em %s" % (label, key, tipo))
            for key in REQUIRED.get(tipo, []):
                _need(errors, rec, key)
        for key in MUST_BE_NAO:
            if key in rec and rec[key] != "não":
                errors.append("%s: %s tem de ser não" % (label, key))
        if tipo == "hipotese" and rec.get("status") and rec["status"] not in STATUS:
            errors.append("%s: status %r inválido" % (label, rec["status"]))
        if tipo == "hipotese" and rec.get("valor") and not VALOR.fullmatch(rec["valor"]):
            errors.append("%s: valor %r não está em reais" % (label, rec["valor"]))
        if tipo == "preferencia" and rec.get("de_quem") and rec["de_quem"] not in {"dono", "cliente", "outra"}:
            errors.append("%s: de_quem %r inválido" % (label, rec["de_quem"]))
        if tipo == "prioridade":
            if rec.get("escala") and rec["escala"] != "1-5":
                errors.append("%s: escala %r tem de ser 1-5" % (label, rec["escala"]))
            nota, anterior = rec.get("nota"), rec.get("nota_anterior")
            if nota and nota != "nenhuma" and nota not in {"1", "2", "3", "4", "5"}:
                errors.append("%s: nota %r fora de 1 a 5" % (label, nota))
            if anterior and anterior != "nenhuma" and anterior not in {"1", "2", "3", "4", "5"}:
                errors.append("%s: nota_anterior %r fora de 1 a 5" % (label, anterior))
        if tipo == "permissao" and rec.get("acao") and rec["acao"] not in {"pesquisar", "construir"}:
            errors.append("%s: acao %r inválida" % (label, rec["acao"]))
        if tipo == "permissao" and rec.get("situacao") and rec["situacao"] not in {"concedida", "recusada"}:
            errors.append("%s: situacao %r inválida" % (label, rec["situacao"]))
        if tipo == "restricao" and rec.get("substitui") and not rec.get("autoridade_citada"):
            errors.append("%s: troca de restrição sem autoridade_citada" % label)
        if tipo == "meta" and rec.get("completo") and rec["completo"] not in {"sim", "não"}:
            errors.append("%s: completo %r inválido" % (label, rec["completo"]))

    for rec in records:
        if rec.get("tipo") != "restricao" or not rec.get("substitui"):
            continue
        label = rec.get("id") or ("bloco " + rec["_bloco"])
        previous = by_id.get(rec["substitui"])
        if not previous or previous.get("tipo") != "restricao":
            errors.append("%s: substitui um id que não é restrição" % label)
            continue
        if rec.get("autoridade_citada") != previous.get("autoridade_pra_mudar"):
            errors.append("%s: autoridade_citada não é quem pode mudar %s" % (label, rec["substitui"]))
    for rec in records:
        if rec.get("tipo") != "decisao":
            continue
        label = rec.get("id") or ("bloco " + rec["_bloco"])
        research = by_id.get(rec.get("pesquisar_id", ""))
        build = by_id.get(rec.get("construir_id", ""))
        if rec.get("pesquisar_id") and (not research or research.get("acao") != "pesquisar"):
            errors.append("%s: pesquisar_id não aponta pra uma permissão de pesquisar" % label)
        if rec.get("construir_id") and (not build or build.get("acao") != "construir"):
            errors.append("%s: construir_id não aponta pra uma permissão de construir" % label)
        if rec.get("pesquisar_id") and rec.get("pesquisar_id") == rec.get("construir_id"):
            errors.append("%s: pesquisar e construir são a mesma permissão" % label)
    return errors


def validate_example(text, records):
    errors = []
    if EXECUTION_LINE not in text:
        errors.append("exemplo sem a frase de que o arquivo não é ordem de executar")
    for word in ("FICTÍCIO", "HIPOTÉTICO", "R$", "America/Sao_Paulo", "versão exclusiva", "cliente grande"):
        if word not in text:
            errors.append("exemplo sem %r" % word)
    if "Nenhuma fala deste arquivo foi dita por uma pessoa real." not in text:
        errors.append("exemplo sem o aviso de que as falas são inventadas")
    kinds = {rec.get("tipo") for rec in records}
    for tipo in ("fato", "hipotese", "preferencia", "restricao", "objetivo", "prioridade", "permissao", "decisao"):
        if tipo not in kinds:
            errors.append("exemplo sem registro do tipo %s" % tipo)
    changed = [
        rec for rec in records
        if rec.get("tipo") == "prioridade" and rec.get("nota_anterior") not in (None, "", "nenhuma")
        and rec.get("nota") != rec.get("nota_anterior")
    ]
    if not changed:
        errors.append("exemplo sem mudança de nota com a nota anterior")
    client = [rec for rec in records if rec.get("tipo") == "preferencia" and rec.get("de_quem") == "cliente"]
    if not client:
        errors.append("exemplo sem preferência de cliente")
    actions = {rec.get("acao") for rec in records if rec.get("tipo") == "permissao"}
    if actions != {"pesquisar", "construir"}:
        errors.append("exemplo não separa permissão de pesquisar e de construir")
    refused = [
        rec for rec in records
        if rec.get("tipo") == "permissao" and rec.get("acao") == "construir" and rec.get("situacao") == "recusada"
    ]
    if not refused:
        errors.append("exemplo não recusa a permissão de construir")
    exclusive = [rec for rec in records if rec.get("tipo") == "restricao" and "exclusiv" in rec.get("texto", "")]
    if not exclusive:
        errors.append("exemplo sem restrição de versão exclusiva")
    return errors


def check_text(text, example=False):
    records, errors = parse_blocks(text)
    if not records:
        errors.append("nenhum bloco registro")
    errors.extend(validate_records(records))
    if example:
        errors.extend(validate_example(text, records))
    return errors


def main(argv):
    example = False
    args = list(argv[1:])
    if args and args[0] == "--example":
        example = True
        args = args[1:]
    if len(args) != 1:
        print("uso: check_registro.py [--example] <arquivo>", file=sys.stderr)
        return 2
    text = open(args[0], encoding="utf-8").read()
    errors = check_text(text, example=example)
    for error in errors:
        print("error: " + error)
    if errors:
        print("%s erro(s)" % len(errors))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
