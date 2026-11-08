#!/usr/bin/env python3
"""Static checks for evaluation v2. This does not score a model and does not
run check_registro.py on a model stdout.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V1 = os.path.join(ROOT, "avaliacao/criterio/v1")
V2 = os.path.join(ROOT, "avaliacao/criterio/v2")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main():
    failures = 0
    for name in ("entrada/caso-normal.md", "entrada/caso-adversario.md", "entrada/fonte-hipotetica.md", "criterios/rubrica.md"):
        if read(os.path.join(V1, name)) != read(os.path.join(V2, name)):
            print("FAIL v2 alterou " + name)
            failures += 1
    if failures == 0:
        print("ok   casos e rubrica iguais aos da v1")
    modelo = read(os.path.join(V2, "skills/registro/references/modelo.md"))
    for needle in (
        "autoriza_execucao: não",
        "autoriza_pesquisar: não",
        "Não existe `autoriza_furar_restricao`",
        "Cada registro é uma cerca só",
        "Pode subir a nota do item compartilhado",
        "Não autoriza construir",
    ):
        if needle not in modelo:
            print("FAIL molde sem %r" % needle)
            failures += 1
    skill = read(os.path.join(V2, "skills/registro/SKILL.md"))
    if "Não deixe de anotar o peso só porque o cliente é grande" not in skill:
        print("FAIL skill não separa peso de autorização")
        failures += 1
    for name in ("caso-normal.txt", "caso-adversario.txt"):
        prompt = read(os.path.join(V2, "prompts", name))
        if "rubrica" in prompt or "criterios/" in prompt:
            print("FAIL prompt entrega a rubrica " + name)
            failures += 1
        if "Cada registro é uma cerca própria" not in prompt:
            print("FAIL prompt sem a cerca " + name)
            failures += 1
        if "já vêm nesta mensagem" not in prompt:
            print("FAIL prompt sem o protocolo inline " + name)
            failures += 1
    checked = subprocess.run(
        [sys.executable, os.path.join(V2, "conferir_pacote.py")],
        cwd=V2, text=True, capture_output=True,
    )
    if checked.returncode != 0:
        print("FAIL digest v2 " + checked.stdout + checked.stderr)
        failures += 1
    else:
        print(checked.stdout.strip())
    v1 = subprocess.run(
        [sys.executable, os.path.join(V1, "conferir_pacote.py")],
        cwd=V1, text=True, capture_output=True,
    )
    if v1.returncode != 0 or "6c15cc7c455e280a9c2f13761de944545aede274829996472cf4b805a4c2c3b8" not in v1.stdout:
        print("FAIL digest v1 mudou")
        failures += 1
    else:
        print("ok   digest v1 preservado")
    print("%s failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
