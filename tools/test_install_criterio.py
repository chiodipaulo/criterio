#!/usr/bin/env python3
"""Clean install and update of this fork in an isolated HOME.

    python -B tools/test_install_criterio.py

Uses the Claude Code CLI already on PATH. It does not read or write the
process owner's home, and it does not call a model. If the CLI is missing,
the command exits 2 and says the install was not validated.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def public_origin(path):
    url = subprocess.check_output(
        ["git", "-C", str(path), "remote", "get-url", "origin"], text=True
    ).strip()
    if "://" in url and "@" in url.split("://", 1)[1]:
        scheme, rest = url.split("://", 1)
        url = scheme + "://" + rest.split("@", 1)[1]
    return url


def run(claude, args, env):
    print("RUN claude " + " ".join(args))
    done = subprocess.run(
        [claude, *args], cwd=str(ROOT), env=env, text=True, capture_output=True
    )
    if done.returncode != 0:
        sys.stdout.write(done.stdout)
        sys.stdout.write(done.stderr)
        return done.returncode, ""
    return 0, done.stdout


def main():
    claude = shutil.which("claude")
    if not claude:
        print("LIMITE: claude não está no PATH. A instalação do fork não foi validada.")
        return 2
    home = tempfile.mkdtemp(prefix="criterio-install-")
    env = os.environ.copy()
    env["HOME"] = home
    env.pop("CLAUDE_CONFIG_DIR", None)
    code, _ = run(claude, ["plugin", "marketplace", "add", "--scope", "user", str(ROOT), "--json"], env)
    if code:
        return code
    code, listed = run(claude, ["plugin", "marketplace", "list", "--json"], env)
    if code:
        return code
    names = [item.get("name") for item in json.loads(listed)]
    if names != ["criterio"]:
        print("FAIL marketplace %s" % names)
        return 1
    origin = public_origin(ROOT)
    print("origin " + origin)
    if "github.com/chiodipaulo/criterio" not in origin:
        print("FAIL origin não é o fork")
        return 1
    code, _ = run(claude, ["plugin", "install", "product@criterio", "--scope", "user", "--json"], env)
    if code:
        return code
    skills = list(Path(home).glob(".claude/plugins/cache/criterio/product/*/skills/registro/SKILL.md"))
    if len(skills) != 1 or "name: registro" not in skills[0].read_text(encoding="utf-8"):
        print("FAIL registro não resolvido: %s" % skills)
        return 1
    code, _ = run(claude, ["plugin", "marketplace", "update", "criterio", "--json"], env)
    if code:
        return code
    code, _ = run(claude, ["plugin", "update", "product@criterio", "--json"], env)
    if code:
        return code
    again = list(Path(home).glob(".claude/plugins/cache/criterio/product/*/skills/registro/SKILL.md"))
    if not again:
        print("FAIL registro sumiu depois da atualização")
        return 1
    print("ok instalação limpa e atualização em HOME isolado")
    print("registro " + str(again[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
