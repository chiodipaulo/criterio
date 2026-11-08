#!/usr/bin/env python3
"""Check that the evaluation bundle bytes match manifesto.json.

    python3 conferir_pacote.py
    python3 conferir_pacote.py --gravar

The manifesto lists every file except itself and except result folders under
saida/. Adding a model output does not change the digest.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFESTO = os.path.join(ROOT, "manifesto.json")
SKILLS_COMMIT = "c28b63a649edb337669cee40850bacf5193d1611"


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def included(path):
    name = rel(path)
    if name == "manifesto.json":
        return False
    if name.startswith("saida/") and name != "saida/LEIA-ME.md" and name != "saida/metadados.modelo.json":
        return False
    return True


def files():
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if included(path):
                found.append(path)
    return sorted(found, key=rel)


def digest_of(entries):
    body = "".join("%s\n%s\n" % (name, entries[name]) for name in sorted(entries))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def hashes():
    entries = {}
    for path in files():
        data = open(path, "rb").read()
        entries[rel(path)] = hashlib.sha256(data).hexdigest()
    return entries


def gravar():
    entries = hashes()
    payload = {
        "versao": 1,
        "nome": "avaliacao-criterio",
        "skills_commit": SKILLS_COMMIT,
        "digest": digest_of(entries),
        "arquivos": entries,
    }
    with open(MANIFESTO, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(payload["digest"])
    return 0


def verificar():
    if not os.path.isfile(MANIFESTO):
        print("manifesto.json ausente")
        return 1
    payload = json.load(open(MANIFESTO, encoding="utf-8"))
    entries = hashes()
    errors = []
    if payload.get("skills_commit") != SKILLS_COMMIT:
        errors.append("skills_commit mudou")
    if payload.get("arquivos") != entries:
        errors.append("lista de arquivos não bate com a pasta")
    if payload.get("digest") != digest_of(entries):
        errors.append("digest não bate")
    if errors:
        print("\n".join(errors))
        return 1
    print("ok " + payload["digest"])
    return 0


if __name__ == "__main__":
    sys.exit(gravar() if "--gravar" in sys.argv[1:] else verificar())
