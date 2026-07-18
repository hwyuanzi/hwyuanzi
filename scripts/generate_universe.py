#!/usr/bin/env python3
"""Shuffle the quote order in universe_100.svg without using JavaScript."""

from __future__ import annotations

import random
import re
from pathlib import Path

SVG_PATH = Path(__file__).resolve().parents[1] / "universe_100.svg"
START = "<!-- QUOTES_START -->"
END = "<!-- QUOTES_END -->"
SLOT_SECONDS = 7


def main() -> None:
    svg = SVG_PATH.read_text(encoding="utf-8")
    before, remainder = svg.split(START, 1)
    block, after = remainder.split(END, 1)

    groups = re.findall(
        r'    <g class="quote-container".*?\n    </g>',
        block,
        flags=re.DOTALL,
    )
    if len(groups) < 2:
        raise RuntimeError(f"Expected multiple quote groups, found {len(groups)}")

    random.SystemRandom().shuffle(groups)
    refreshed: list[str] = []
    for index, group in enumerate(groups):
        group = re.sub(
            r'opacity="[01]"',
            f'opacity="{1 if index == 0 else 0}"',
            group,
            count=1,
        )
        group = re.sub(
            r'animation-delay:\d+s',
            f'animation-delay:{index * SLOT_SECONDS}s',
            group,
            count=1,
        )
        group = re.sub(
            r'data-quote="\d+"',
            f'data-quote="{index + 1}"',
            group,
            count=1,
        )
        refreshed.append(group)

    updated = before + START + "\n" + "\n".join(refreshed) + "\n    " + END + after
    SVG_PATH.write_text(updated, encoding="utf-8")
    print(f"Shuffled {len(refreshed)} quotes in {SVG_PATH.name}.")


if __name__ == "__main__":
    main()
