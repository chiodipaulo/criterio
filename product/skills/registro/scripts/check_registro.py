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
import html
import os
import re
import sys
from html.parser import HTMLParser
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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
        "item", "nota", "escala", "nota_anterior", "anterior_id", "autoriza_versao_exclusiva",
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
COMPARACAO_DE_TEXTO_NAO_AUTENTICA = (
    "Comparar autor e autoridade como texto não autentica a permissão "
    "e não dispensa o ok de uma pessoa na sessão."
)
NOTES = {"1", "2", "3", "4", "5"}
CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)


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


def _record_from_lines(body, index, errors):
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
    return rec


class _RegistroHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.articles, self.errors, self.current = [], [], None
        self.mode, self.key, self.buf = None, None, []

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        if tag == "article" and "registro" in classes:
            self.current = {}
        elif self.current is not None and tag in ("dt", "dd"):
            self.mode, self.buf = tag, []

    def handle_data(self, data):
        if self.mode:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "dt" and self.mode == "dt":
            self.key = "".join(self.buf).strip()
            self.mode = None
        elif tag == "dd" and self.mode == "dd":
            if self.key:
                value = "".join(self.buf).strip()
                if self.key in self.current:
                    bloco = str(len(self.articles) + 1)
                    self.errors.append("bloco %s: campo repetido %s" % (bloco, self.key))
                else:
                    self.current[self.key] = value
            self.key, self.mode = None, None
        elif tag == "article" and self.current is not None:
            self.current["_bloco"] = str(len(self.articles) + 1)
            self.articles.append(self.current)
            self.current = None


def parse_blocks(text):
    """Return (records, errors) from markdown fences or HTML articles, not both."""
    records, errors = [], []
    bodies = FENCE.findall(text)
    masked = CODE_FENCE.sub("", text)
    parser = _RegistroHTML()
    parser.feed(masked)
    if bodies and parser.articles:
        errors.append("duas representações no mesmo arquivo")
        return records, errors
    if bodies:
        for index, body in enumerate(bodies, 1):
            records.append(_record_from_lines(body, index, errors))
        return records, errors
    errors.extend(parser.errors)
    return parser.articles, errors


def render_markdown(records):
    blocks = []
    for rec in records:
        lines = ["```registro"]
        for key, value in rec.items():
            if key.startswith("_"):
                continue
            lines.append("%s: %s" % (key, value))
        lines.append("```")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def render_html(records):
    chunks = []
    for rec in records:
        rows = []
        for key, value in rec.items():
            if key.startswith("_"):
                continue
            rows.append("<dt>%s</dt><dd>%s</dd>" % (html.escape(key), html.escape(value)))
        chunks.append("<article class=\"registro\">\n<dl>\n%s\n</dl>\n</article>" % "\n".join(rows))
    return "\n".join(chunks)


def same_records(left, right):
    def plain(rec):
        return {key: value for key, value in rec.items() if not key.startswith("_")}
    return [plain(rec) for rec in left] == [plain(rec) for rec in right]


def meaningful(value):
    text = (value or "").strip()
    return len(text) >= 12 and any(ch.isalpha() for ch in text)


def valid_zone(value):
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        return False
    return True


def date_tuple(value):
    day, month, year = (int(part) for part in value.split("/"))
    return (year, month, day)


def local_source_ok(fonte, base_dir):
    if not fonte.startswith("local: "):
        return False, "fonte local precisa do prefixo local:"
    rel = fonte[len("local: "):].strip()
    parts = rel.split("/")
    if not rel or rel.startswith("/") or any(part in ("", ".", "..") for part in parts):
        return False, "fonte local não sai da pasta do registro"
    if not base_dir:
        return False, "fonte local sem pasta pra conferir"
    root = os.path.realpath(base_dir)
    full = os.path.realpath(os.path.join(root, rel))
    if full != root and not full.startswith(root + os.sep):
        return False, "fonte local não sai da pasta do registro"
    if not os.path.isfile(full):
        return False, "fonte local não encontra o arquivo"
    return True, ""


def fact_source_ok(fonte, base_dir):
    fonte = (fonte or "").strip()
    if fonte.startswith("https://") or fonte.startswith("http://"):
        host = fonte.split("://", 1)[1].split("/", 1)[0]
        if host and "." in host:
            return True, ""
        return False, "fonte de fato sem endereço rastreável"
    if fonte.startswith("local:"):
        return local_source_ok(fonte, base_dir)
    return False, "fonte de fato sem endereço rastreável"


def _need(errors, rec, key):
    if not rec.get(key):
        errors.append("%s: falta %s" % (rec.get("id") or ("bloco " + rec["_bloco"]), key))
        return False
    return True


def validate_records(records, base_dir=None):
    errors, by_id = [], {}
    for rec in records:
        label = rec.get("id") or ("bloco " + rec.get("_bloco", "?"))
        for key in ("id", "tipo", "autor", "motivo", "fonte", "data", "fuso", "texto"):
            _need(errors, rec, key)
        if rec.get("texto") is not None and not meaningful(rec.get("texto")):
            errors.append("%s: texto sem conteúdo" % label)
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
        if rec.get("fuso") and not valid_zone(rec["fuso"]):
            errors.append("%s: fuso %r não é um nome IANA" % (label, rec["fuso"]))
        if tipo == "fato" and rec.get("fonte"):
            ok_source, why = fact_source_ok(rec["fonte"], base_dir)
            if not ok_source:
                errors.append("%s: %s" % (label, why))
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
            if nota == "nenhuma":
                errors.append("%s: nota não pode ser nenhuma" % label)
            elif nota and nota not in NOTES:
                errors.append("%s: nota %r fora de 1 a 5" % (label, nota))
            if anterior and anterior != "nenhuma" and anterior not in NOTES:
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
    errors.extend(priority_chain(records, by_id))
    return errors


def priority_chain(records, by_id):
    errors, starts, followed = [], {}, {}
    for rec in records:
        if rec.get("tipo") != "prioridade":
            continue
        label = rec.get("id") or ("bloco " + rec["_bloco"])
        anterior = rec.get("nota_anterior")
        if anterior == "nenhuma":
            if rec.get("anterior_id"):
                errors.append("%s: início não aponta pra outro registro" % label)
            item = rec.get("item")
            if item in starts:
                errors.append("%s: dois inícios pro mesmo item" % item)
            elif item:
                starts[item] = rec
            continue
        if anterior not in NOTES:
            continue
        prev_id = rec.get("anterior_id")
        if not prev_id:
            errors.append("%s: sem o registro anterior" % label)
            continue
        prev = by_id.get(prev_id)
        if not prev or prev.get("tipo") != "prioridade":
            errors.append("%s: sem o registro anterior" % label)
            continue
        if prev.get("item") != rec.get("item"):
            errors.append("%s: item diferente do registro anterior" % label)
        if prev.get("nota") != anterior:
            errors.append("%s: nota anterior não é a nota do registro %s" % (label, prev_id))
        if prev_id in followed:
            errors.append("%s: o registro anterior já tem continuação" % label)
        followed[prev_id] = label
        if valid_date(prev.get("data", "")) and valid_date(rec.get("data", "")):
            if date_tuple(rec["data"]) < date_tuple(prev["data"]):
                errors.append("%s: ordem da data quebra a cadeia" % label)
    for rec in records:
        if rec.get("tipo") != "prioridade":
            continue
        message = _chain_end(rec, by_id)
        if message:
            errors.append(message)
    return errors


def _valid_start(rec):
    return (
        rec.get("tipo") == "prioridade"
        and rec.get("nota_anterior") == "nenhuma"
        and not rec.get("anterior_id")
        and rec.get("nota") in NOTES
    )


def _chain_end(rec, by_id):
    """Each score must reach a real first record. A loop, including a self-link, does not."""
    label = rec.get("id") or ("bloco " + rec.get("_bloco", "?"))
    seen = []
    cursor = rec
    while True:
        current = cursor.get("id")
        if current and current in seen:
            return "%s: ciclo na cadeia de prioridade" % label
        if current:
            seen.append(current)
        if _valid_start(cursor):
            return None
        prev_id = cursor.get("anterior_id")
        if not prev_id or prev_id == current:
            return "%s: ciclo na cadeia de prioridade" % label if prev_id == current else (
                "%s: a cadeia não termina num início" % label)
        nxt = by_id.get(prev_id)
        if not nxt or nxt.get("tipo") != "prioridade":
            return "%s: a cadeia não termina num início" % label
        cursor = nxt


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


def check_text(text, example=False, base_dir=None):
    records, errors = parse_blocks(text)
    if not records:
        errors.append("nenhum bloco registro")
    errors.extend(validate_records(records, base_dir=base_dir))
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
    errors = check_text(text, example=example, base_dir=os.path.dirname(os.path.abspath(args[0])))
    for error in errors:
        print("error: " + error)
    if errors:
        print("%s erro(s)" % len(errors))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
