#!/usr/bin/env python3
"""Check QA Markdown for the repository's human-docs rules."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA_ROOT = ROOT / "Quality Assurance Officer"
BANNED = {
    r"\bdelve\b": "use read, inspect, or name the action",
    r"\brobust\b": "state the measured behavior",
    r"\bcomprehensive\b": "state the exact scope",
    r"\bcrucial\b": "state whether it blocks release",
    r"\bpivotal\b": "state the concrete effect",
    r"\bleverage\b": "use use",
    r"\butilize\b": "use use",
    r"\bfacilitate\b": "name the action",
    r"\blandscape\b": "name the system or corpus",
    r"\bshowcase\b": "use display or remove",
    r"\bfoster\b": "name the mechanism",
    r"\bcultivate\b": "name the mechanism",
    r"\bIn conclusion\b": "delete the conclusion opener",
    r"\bTo summarize\b": "delete the summary opener",
    r"\bIt is worth noting\b": "state the fact",
    r"\bThis document serves\b": "state the scope",
}


def prose_without_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def main() -> int:
    failures = []
    files = sorted(QA_ROOT.glob("*.md"))

    for path in files:
        text = prose_without_code(path.read_text(encoding="utf-8"))
        for pattern, advice in BANNED.items():
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{path.name}:{line}: {match.group(0)!r}; {advice}")

        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.startswith("#"):
                continue
            heading = line.lstrip("#").strip()
            words = [
                word for word in re.findall(r"[A-Za-z]+", heading) if len(word) > 2
            ]
            if len(words) < 4:
                continue
            title_case_words = sum(word[0].isupper() for word in words)
            if title_case_words / len(words) >= 0.8:
                failures.append(
                    f"{path.name}:{line_number}: heading appears title-cased: {heading}"
                )

    if failures:
        print("\n".join(failures))
        return 1

    print(f"Documentation style PASS: {len(files)} QA Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
