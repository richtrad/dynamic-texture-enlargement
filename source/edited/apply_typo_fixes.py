"""Create a conservative typo-only copy of the recovered LaTeX source."""

from __future__ import annotations

import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
source = root / "original" / "13sccg_DT.tex"
target = Path(__file__).resolve().parent / "13sccg_DT_typos.tex"

# Mechanical spelling fixes and a few unambiguous local agreement errors.
# The archival source remains byte-for-byte unchanged; ambiguous prose and
# scientific wording are intentionally left for author review.
replacements = [
    ("synthetize", "synthesize"),
    ("can finds", "can find"),
    ("archieved", "achieved"),
    ("rewrited", "rewritten"),
    ("paremeters", "parameters"),
    ("overhelmed", "overwhelmed"),
    ("approache", "approach"),
    ("noteciably", "noticeably"),
    ("apporaches", "approaches"),
    ("parches", "patches"),
    ("arror", "error"),
    ("drived by", "derived by"),
    ("homogenous", "homogeneous"),
    ("danamic", "dynamic"),
    ("freme", "frame"),
    ("soution", "solution"),
    ("simillar", "similar"),
    ("offseted", "offset"),
    ("horisontally", "horizontally"),
    ("horisontal", "horizontal"),
    ("dissapears", "disappears"),
    ("extremply", "extremely"),
    ("uniquess", "uniqueness"),
    ("unles", "unless"),
    ("fing greater", "find greater"),
    ("whach", "which"),
    ("consistenly", "consistently"),
    ("bee seen", "be seen"),
]

# The historical file contains a few legacy Windows-1250 bytes in comments.
# Decode those conservatively; the byte-preserved archival file is untouched.
text = source.read_text(encoding="cp1250", errors="replace")
counts: list[tuple[str, str, int]] = []
for old, new in replacements:
    pattern = rf"(?<!\w){re.escape(old)}(?!\w)"
    text, count = re.subn(pattern, new, text)
    if count:
        counts.append((old, new, count))

target.write_text(text, encoding="utf-8")
log = [
    "# Typo-only source working copy",
    "",
    "Generated from `source/original/13sccg_DT.tex`. The archival source is",
    "unchanged. Only the listed mechanical corrections were applied; no",
    "equation, number, citation key, figure, table, or experimental claim was",
    "changed. Ambiguous prose remains for author review.",
    "",
    "| Original | Replacement | Occurrences |",
    "| --- | --- | ---: |",
]
log.extend(f"| `{old}` | `{new}` | {count} |" for old, new, count in counts)
log.extend(
    [
        "",
        "The file still references the historical `sty/`, `img/`, and `BIB/`",
        "directories described in `source/original/SOURCE_INFO.md`; it is not",
        "a self-contained build until those dependencies are recovered.",
    ]
)
(target.parent / "CHANGELOG.md").write_text("\n".join(log) + "\n", encoding="utf-8")
print(f"wrote {target}")
print(f"applied {len(counts)} replacement rules")
