#!/usr/bin/env python3
"""Structural checks for the Critério fork layer.

    python -B tools/test_criterio.py

These checks read files. They do not call a model and they do not treat a
green run as proof that a model followed a skill.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = b"<!-- upstream-readme -->\n"
README_SHA = "3137b0f994fcaba8b4e22909897b5857a0363e35ceb6ea9c713f189636c4ebf1"
LICENSE_SHA = "a2c922f9b81b4f40347ddfa79c38eda0f1278b5a6d108bd4099b4da254c774ee"

UPSTREAM_SKILLS = [
    "agent-harness/skills/agent-instructions",
    "agent-harness/skills/flight-deck",
    "agent-harness/skills/guardrail-hooks",
    "agent-harness/skills/handover",
    "agent-harness/skills/retro",
    "agent-harness/skills/windows-agent-shell",
    "agent-teams/skills/claude-agents",
    "agent-teams/skills/codex-agents",
    "agent-teams/skills/delegation",
    "agent-teams/skills/grok-agents",
    "ai-shipping/skills/code-review",
    "ai-shipping/skills/derive-tests",
    "ai-shipping/skills/document-app",
    "ai-shipping/skills/independent-review",
    "ai-shipping/skills/intended-vs-implemented",
    "ai-shipping/skills/performance-audit-static",
    "ai-shipping/skills/release-gate",
    "ai-shipping/skills/security-audit-static",
    "ai-shipping/skills/ship-check",
    "ai-shipping/skills/shipping-artifacts",
    "ai-shipping/skills/test-harness",
    "app-stack/skills/app-lifecycle",
    "app-stack/skills/chatgpt-plugin",
    "app-stack/skills/clerk-production",
    "app-stack/skills/embedded-agents-agent-sdk",
    "app-stack/skills/embedded-agents-messages-api",
    "app-stack/skills/environments",
    "app-stack/skills/legal-pages",
    "app-stack/skills/mcp-server",
    "app-stack/skills/product-analytics",
    "app-stack/skills/saas-authorization",
    "app-stack/skills/supabase-production",
    "app-stack/skills/transactional-email",
    "app-stack/skills/ui-design",
    "app-stack/skills/uptime-monitoring",
    "product/skills/beachhead-segment",
    "product/skills/competitor-analysis",
    "product/skills/growth-loops",
    "product/skills/market-segments",
    "product/skills/propose",
    "product/skills/start-here",
    "product/skills/value-curve",
    "product/skills/value-proposition",
    "work-humanizer/skills/work-humanizer",
]

MATRIX = {
    "Leitura de SKILL.md como texto": "testado aqui",
    "Instalação limpa e atualização": "testado aqui",
    "Manifesto claude plugin validate": "testado aqui",
    "Claude Code numa sessão de pessoa": "só documentado",
    "Codex": "só documentado",
    "Gemini CLI": "só documentado",
    "API, fornecedor ou conta": "não suportado",
    "Ferramenta universal": "não suportado",
    "Lint como prova semântica": "não suportado",
    "Uso comportamental com modelos": "experimental fechada, revisão humana obrigatória",
}

BANNERS = [
    "app-stack/README.md",
    "agent-teams/README.md",
    "ai-shipping/README.md",
    "agent-harness/README.md",
]

PHRASES = [
    "Critério",
    "https://github.com/phuryn/product-engineering",
    "chiodipaulo/criterio",
    "Pawel Huryn",
    "Paulo Chiodi",
    "MIT",
    "LICENSE.md",
    "Este fork não promete funcionar em qualquer modelo.",
    "Nenhum modelo foi chamado",
    "Não há atualização automática.",
    "claude plugin marketplace remove product-engineering",
    "product@criterio",
    "Portátil",
    "`registro`",
    "/product:registro",
    "docs/escopo.md",
    "44 skills",
    "Os comandos do texto original instalam `phuryn/product-engineering`, não este fork.",
    "claude plugin validate",
    "2.1.311",
    "avaliacao/criterio/v1",
]

def _word(*parts):
    return "".join(parts)


FORBIDDEN = [
    "funciona em qualquer modelo",
    "compatível com qualquer modelo",
    "testado em qualquer modelo",
    "todos os modelos",
    "todos os CLIs",
    _word("Stay", "green"),
    _word("Ask", "One"),
    _word("afk", "pilot"),
    _word("product", "compass"),
]


def read(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def fail(message):
    print("FAIL " + message)
    return 1


def ok(message):
    print("ok   " + message)
    return 0


def strip_fences(text):
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def links_in(text):
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def check_links(rel, text):
    failures = 0
    base = os.path.dirname(os.path.join(ROOT, rel))
    for target in links_in(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0]
        if not path:
            continue
        full = os.path.normpath(os.path.join(base, path))
        if not os.path.exists(full):
            failures += fail("%s: link quebrado %s" % (rel, target))
    return failures


def table_status(preface):
    found = {}
    for line in preface.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= set("-: "):
            continue
        found[cells[0]] = cells[1]
    return found


def main():
    failures = 0
    if len(UPSTREAM_SKILLS) != 44:
        failures += fail("a lista congelada não tem 44 skills")

    license_bytes = open(os.path.join(ROOT, "LICENSE.md"), "rb").read()
    if hashlib.sha256(license_bytes).hexdigest() != LICENSE_SHA:
        failures += fail("LICENSE.md mudou. A licença MIT tem de ficar inteira")
    else:
        failures += ok("LICENSE.md intacto")

    readme = open(os.path.join(ROOT, "README.md"), "rb").read()
    if MARKER not in readme:
        return fail("README sem o marcador do texto original")
    preface_b, tail = readme.split(MARKER, 1)
    if hashlib.sha256(tail).hexdigest() != README_SHA:
        failures += fail("o texto original do README não está byte a byte")
    else:
        failures += ok("README de origem preservado")
    preface = preface_b.decode("utf-8")

    missing = [phrase for phrase in PHRASES if phrase not in preface]
    for phrase in missing:
        failures += fail("entrada sem %r" % phrase)
    if not missing:
        failures += ok("frases da entrada")

    prose = strip_fences(preface)
    if ";" in prose:
        failures += fail("ponto e vírgula na prosa da entrada")
    else:
        failures += ok("entrada sem ponto e vírgula na prosa")
    paras = re.findall(r"\bpara\b", prose, flags=re.IGNORECASE)
    if paras:
        failures += fail("a entrada usa 'para' %s vez(es)" % len(paras))
    else:
        failures += ok("entrada usa pra")

    leaked = [phrase for phrase in FORBIDDEN if phrase.lower() in preface.lower()]
    for phrase in leaked:
        failures += fail("entrada contém %r" % phrase)
    if not leaked:
        failures += ok("entrada sem promessa larga e sem nomes de produto do autor")

    status = table_status(preface)
    for label, expected in MATRIX.items():
        got = status.get(label)
        if got != expected:
            failures += fail("matriz %r está %r, esperado %r" % (label, got, expected))
    if all(status.get(label) == expected for label, expected in MATRIX.items()):
        failures += ok("matriz de suporte")
    tested = [line for line in preface.splitlines() if line.startswith("| Leitura de SKILL.md")]
    if not tested or "Nenhum modelo foi chamado" not in tested[0]:
        failures += fail("a linha testada não diz que nenhum modelo foi chamado")

    failures += check_links("README.md", preface)
    failures += check_links("docs/escopo.md", read("docs/escopo.md"))

    full = readme.decode("utf-8")
    for skill in UPSTREAM_SKILLS:
        name = skill.rsplit("/", 1)[-1]
        folder = os.path.join(ROOT, skill, "SKILL.md")
        if not os.path.isfile(folder):
            failures += fail("skill de origem sumiu: " + skill)
        if "`%s`" % name not in full and "**%s**" % name not in full:
            failures += fail("README não lista %s" % name)
    skill_mds = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir == "avaliacao" or rel_dir.startswith("avaliacao" + os.sep):
            continue
        if "SKILL.md" in filenames and os.path.basename(os.path.dirname(dirpath)) == "skills":
            skill_mds.append(os.path.relpath(os.path.join(dirpath, "SKILL.md"), ROOT))
    if len(skill_mds) != 45:
        failures += fail("esperados 45 SKILL.md, achados %s" % len(skill_mds))
    else:
        failures += ok("44 skills de origem e registro")

    registro = read("product/skills/registro/SKILL.md")
    if "disable-model-invocation: true" not in registro:
        failures += fail("registro entrou na lista automática e estoura o teto de 6000 caracteres")
    else:
        failures += ok("registro é iniciado pela pessoa")
    policy = read("product/skills/registro/agents/openai.yaml")
    if "allow_implicit_invocation: false" not in policy:
        failures += fail("registro sem a trava do Codex")
    if "## How you can tell it worked" not in registro:
        failures += fail("registro sem a seção de evidência")

    for rel in ("product/skills/propose/SKILL.md", "product/skills/start-here/SKILL.md"):
        text = read(rel)
        if "/product:registro" not in text:
            failures += fail("%s não aponta o comando" % rel)
        section = text.split("### Fork Critério", 1)
        if len(section) != 2:
            failures += fail("%s sem a ponte do fork" % rel)
            continue
        body = re.split(r"\n#{1,3} ", section[1], maxsplit=1)[0]
        for word in ("fato", "hipótese", "preferência", "restrição", "objetivo"):
            if word not in body:
                failures += fail("%s sem %s" % (rel, word))
        if "\bpara\b" and re.search(r"\bpara\b", body, flags=re.IGNORECASE):
            failures += fail("%s usa para na ponte" % rel)
        if ";" in body:
            failures += fail("%s tem ponto e vírgula na ponte" % rel)
        if "the `registro` skill" in body:
            failures += fail("%s trata registro como skill carregável" % rel)

    outside = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, filename), ROOT)
            if rel.startswith("product/skills/registro/"):
                continue
            if "the `registro` skill" in read(rel):
                outside.append(rel)
    if outside:
        failures += fail("registro nomeado como skill carregável em " + ", ".join(outside))
    else:
        failures += ok("registro não é citado como skill carregável")

    for rel in BANNERS:
        text = read(rel)
        if "O fork não trata este pacote como ferramenta universal." not in text:
            failures += fail("%s sem o aviso de pacote preso a provedor" % rel)
    if all("O fork não trata este pacote como ferramenta universal." in read(rel) for rel in BANNERS):
        failures += ok("avisos dos pacotes presos a provedor")

    escopo = read("docs/escopo.md")
    for phrase in ("Fase 1", "Fases seguintes", "6000", "app-stack", "America/Sao_Paulo", "8bae83d"):
        if phrase not in escopo:
            failures += fail("escopo sem %r" % phrase)
    if ";" in strip_fences(escopo) or re.search(r"\bpara\b", strip_fences(escopo), flags=re.I):
        failures += fail("escopo com para ou ponto e vírgula")
    else:
        failures += ok("escopo")

    for rel in (
        "product/skills/registro/SKILL.md",
        "product/skills/registro/references/modelo.md",
        "product/skills/registro/references/exemplo-escala-miuda.md",
    ):
        text = strip_fences(read(rel))
        if ";" in text or re.search(r"\bpara\b", text, flags=re.I):
            failures += fail("%s com para ou ponto e vírgula na prosa" % rel)
    sys.path.insert(0, os.path.join(ROOT, "product/skills/registro/scripts"))
    import check_registro  # noqa: E402
    example = read("product/skills/registro/references/exemplo-escala-miuda.md")
    errors = check_registro.check_text(
        example, example=True, base_dir=os.path.dirname(os.path.join(ROOT, "product/skills/registro/references/exemplo-escala-miuda.md"))
    )
    if errors:
        failures += fail("exemplo: " + " | ".join(errors))
    else:
        failures += ok("exemplo confere")

    product = read("product/README.md")
    if "`registro`" not in product and "**registro**" not in product:
        failures += fail("product/README.md não lista registro")
    else:
        failures += ok("pacote product lista registro")

    market = json.loads(read(".claude-plugin/marketplace.json"))
    if market.get("name") != "criterio":
        failures += fail("marketplace name %r" % market.get("name"))
    owner = market.get("owner") or {}
    if owner.get("name") != "Paulo Chiodi" or owner.get("url") != "https://github.com/chiodipaulo/criterio":
        failures += fail("owner do marketplace %r" % owner)
    if "email" in owner:
        failures += fail("owner do marketplace tem e-mail")
    if market.get("name") == "criterio" and "email" not in owner:
        failures += ok("marketplace criterio sem e-mail inventado")
    plugins = {item["name"] for item in market.get("plugins", [])}
    if plugins != {"product", "ai-shipping", "agent-teams", "agent-harness", "app-stack", "work-humanizer"}:
        failures += fail("plugins %s" % sorted(plugins))

    ptbr = [
        "product/skills/start-here/references/pt-br.md",
        "product/skills/propose/references/pt-br.md",
        "product/skills/competitor-analysis/references/pt-br.md",
        "product/skills/market-segments/references/pt-br.md",
        "product/skills/beachhead-segment/references/pt-br.md",
        "product/skills/value-proposition/references/pt-br.md",
        "product/skills/value-curve/references/pt-br.md",
    ]
    for rel in ptbr:
        text = read(rel)
        skill = rel.split("/references/")[0] + "/SKILL.md"
        if "references/pt-br.md" not in read(skill):
            failures += fail("%s não aponta o roteiro" % skill)
        prose = strip_fences(text)
        if "R$" not in text or "dd/mm/aaaa" not in text:
            failures += fail("%s sem reais ou data brasileira" % rel)
        if ";" in prose or re.search(r"\bpara\b", prose, flags=re.I):
            failures += fail("%s com para ou ponto e vírgula" % rel)
        if "texto portátil" not in text:
            failures += fail("%s sem a fronteira portátil" % rel)
    if all(os.path.isfile(os.path.join(ROOT, rel)) for rel in ptbr):
        failures += ok("roteiros em português do fluxo")

    bundle = os.path.join(ROOT, "avaliacao/criterio/v1")
    checked = subprocess.run(
        [sys.executable, os.path.join(bundle, "conferir_pacote.py")],
        cwd=bundle, text=True, capture_output=True,
    )
    if checked.returncode != 0:
        failures += fail("pacote de avaliação: " + (checked.stdout + checked.stderr).strip())
    else:
        failures += ok("digest do pacote de avaliação")
    for prompt_name in ("caso-normal.txt", "caso-adversario.txt"):
        prompt = read("avaliacao/criterio/v1/prompts/" + prompt_name)
        if "criterios/" in prompt or "rubrica" in prompt:
            failures += fail(prompt_name + " entrega a rubrica ao modelo")
    if "exemplo-escala-miuda.md" in os.listdir(os.path.join(bundle, "skills/registro/references")):
        failures += fail("o exemplo preenchido entrou no pacote do modelo")

    print("%s failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
