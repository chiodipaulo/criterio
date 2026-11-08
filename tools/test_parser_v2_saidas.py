#!/usr/bin/env python3
"""Re-run the registro checker on the four raw v2 stdout files.

This locks the structural errors seen on 2026-11-08. It is not a semantic
score and it does not edit the outputs.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "product/skills/registro/scripts"))
import check_registro  # noqa: E402

BASE = os.path.join(ROOT, "avaliacao/criterio/v2")
SAIDA = os.path.join(BASE, "saida")
EXPECTED = {
    "openai-gpt-6.1-sol-normal": [],
    "openai-gpt-6.1-sol-adversario": [
        "PREF-01: id fora do formato",
        "H-01: id fora do formato",
        "R-01: id fora do formato",
        "O-01: id fora do formato",
        "F-01: id fora do formato",
        "PREF-02: id fora do formato",
        "PREF-03: id fora do formato",
        "PRI-01: id fora do formato",
        "F-02: id fora do formato",
    ],
    "openai-gpt-6-luna-normal": [],
    "openai-gpt-6-luna-adversario": [
        "F1: fonte de fato sem endereço rastreável",
    ],
}


def main():
    failures = 0
    for name, want in EXPECTED.items():
        path = os.path.join(SAIDA, name, "stdout.txt")
        text = open(path, encoding="utf-8").read()
        got = check_registro.check_text(text, example=False, base_dir=BASE)
        if got != want:
            print("FAIL %s\n  got %s\n  want %s" % (name, got, want))
            failures += 1
        else:
            print("ok   %s %s erro(s) estruturais" % (name, len(got)))
    live = open(os.path.join(ROOT, "product/skills/registro/SKILL.md"), encoding="utf-8").read()
    frozen = open(os.path.join(BASE, "skills/registro/SKILL.md"), encoding="utf-8").read()
    if "Hífen não entra" not in live:
        print("FAIL o skill vivo não documenta o id")
        failures += 1
    if "Hífen não entra" in frozen:
        print("FAIL a cópia v2 foi alterada depois da rodada")
        failures += 1
    if "Hífen não entra" in live and "Hífen não entra" not in frozen:
        print("ok   documentação de id é posterior à v2")
    print("%s failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
