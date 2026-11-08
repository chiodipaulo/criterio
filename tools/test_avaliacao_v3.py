#!/usr/bin/env python3
"""Static checks for evaluation v3. Not a model score."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V1 = os.path.join(ROOT, "avaliacao/criterio/v1")
V2 = os.path.join(ROOT, "avaliacao/criterio/v2")
V3 = os.path.join(ROOT, "avaliacao/criterio/v3")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main():
    failures = 0
    for name in ("entrada/caso-normal.md", "entrada/caso-adversario.md", "entrada/fonte-hipotetica.md", "criterios/rubrica.md"):
        if read(os.path.join(V1, name)) != read(os.path.join(V3, name)):
            print("FAIL v3 alterou " + name)
            failures += 1
    if failures == 0:
        print("ok   casos e rubrica iguais aos da v1")
    checker = os.path.join(ROOT, "product/skills/registro/scripts/check_registro.py")
    bundled = os.path.join(V3, "ferramentas/check_registro.py")
    if read(checker) != read(bundled):
        print("FAIL conferidor do pacote diferente do script do repositório")
        failures += 1
    else:
        print("ok   conferidor versionado igual ao script")
    for name in ("caso-normal.txt", "caso-adversario.txt"):
        prompt = read(os.path.join(V3, "prompts", name))
        for banned in ("rubrica", "criterios/", "check_registro", "notas-do-revisor", "stdout"):
            if banned in prompt:
                print("FAIL prompt contém %s em %s" % (banned, name))
                failures += 1
        if "sem hífen" not in prompt or "local:" not in prompt:
            print("FAIL prompt sem formato de id ou fonte " + name)
            failures += 1
        if "Cada registro é uma cerca própria" not in prompt:
            print("FAIL prompt sem cerca " + name)
            failures += 1
    live = read(os.path.join(ROOT, "product/skills/propose/references/pt-br.md"))
    frozen = read(os.path.join(V2, "skills/propose/references/pt-br.md"))
    phrase = "A primeira versão é concreta mesmo quando falta pesquisa"
    if phrase not in live or phrase not in read(os.path.join(V3, "skills/propose/references/pt-br.md")):
        print("FAIL proposta sem primeira versão concreta")
        failures += 1
    if phrase in frozen:
        print("FAIL a cópia v2 da proposta foi alterada")
        failures += 1
    for folder, needle in ((V1, "6c15cc7c455e280a9c2f13761de944545aede274829996472cf4b805a4c2c3b8"), (V2, "cc58e72e30cac0a71ecf0c73e7cb1ac72ca3404bbcf99565c45544a1d68e9c08")):
        done = subprocess.run([sys.executable, os.path.join(folder, "conferir_pacote.py")], cwd=folder, text=True, capture_output=True)
        if done.returncode != 0 or needle not in done.stdout:
            print("FAIL digest antigo " + folder)
            failures += 1
    v3 = subprocess.run([sys.executable, os.path.join(V3, "conferir_pacote.py")], cwd=V3, text=True, capture_output=True)
    if v3.returncode != 0:
        print("FAIL digest v3 " + v3.stdout + v3.stderr)
        failures += 1
    else:
        print(v3.stdout.strip())
    print("%s failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
