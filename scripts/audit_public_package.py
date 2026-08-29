from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

FORBIDDEN_NAMES = {
    ".env",
    "organic-competitors.csv",
    "organic-keywords.csv",
    "top-pages.csv",
    "evidencias.csv",
    "manifesto-entrega.md",
}

FORBIDDEN_SUFFIXES = {".xlsx", ".xls", ".m4a", ".mp4", ".zip"}

CONTENT_PATTERNS = {
    "caminho local Windows": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "pasta interna Codex": re.compile(r"\\.codex[\\/]", re.IGNORECASE),
    "placeholder": re.compile(r"\ba preencher\b|\bnão iniciado\b", re.IGNORECASE),
    "identificação pessoal interna": re.compile(r"\bÍcaro\b|\bIcaro\b", re.IGNORECASE),
    "aprovação interna": re.compile(
        r"Aprovado por|Rejeitado por|A revisar com|decisão humana registrada|"
        r"revisão humana|aprovação humana|aprovadas? no cockpit",
        re.IGNORECASE,
    ),
    "controle interno datado": re.compile(
        r"Atualizado em \d{2}/\d{2}/\d{4}|Aprovado em \d{2}/\d{2}/\d{4}|"
        r"cloudwalk-gate1-\d{8}",
        re.IGNORECASE,
    ),
    "identificador interno de decisão": re.compile(r"\b(?:D0\d{2}|GB0\d)\b"),
    "aba interna antiga": re.compile(r"\bDecisoes\b"),
    "dependência do ambiente interno": re.compile(r"@oai/artifact-tool", re.IGNORECASE),
    "chave privada": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "token provável": re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}"),
}

TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".py", ".md", ".txt", ".xml", ""}


def main() -> int:
    problems: list[str] = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue

        relative = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES:
            problems.append(f"arquivo proibido: {relative}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"extensão proibida: {relative}")

        if path == SELF or path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in CONTENT_PATTERNS.items():
            if pattern.search(text):
                problems.append(f"{label}: {relative}")

    if problems:
        print("AUDITORIA REPROVADA")
        for problem in problems:
            print(f"- {problem}")
        return 1

    files = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    print(f"AUDITORIA APROVADA - {files} arquivos verificados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
