#!/usr/bin/env python3
"""Apply the Claude-inspired palette and reshuffle profile quotes."""

from __future__ import annotations

import random
import re
from pathlib import Path

SVG_PATH = Path(__file__).resolve().parents[1] / "universe_100.svg"
START = "<!-- QUOTES_START -->"
END = "<!-- QUOTES_END -->"
SLOT_SECONDS = 7

REPLACEMENTS = {
    "A warm liquid-glass profile card inspired by thoughtful editorial design and macOS.": "A cream, terracotta, and dark-cocoa liquid-glass profile card inspired by Claude and macOS.",
    "fill:#FFF8F1; text-anchor:middle;": "fill:#2D2926; text-anchor:middle;",
    "fill:#DCCFC4; text-anchor:middle;": "fill:#655D57; text-anchor:middle;",
    "fill:#B8AB9F; text-anchor:middle;": "fill:#786E67; text-anchor:middle;",
    "fill:#F5ECE4; text-anchor:middle;": "fill:#342F2C; text-anchor:middle;",
    "fill:#BCAFA4; text-anchor:middle;": "fill:#8A6558; text-anchor:middle;",
    '<stop stop-color="#181512"/>': '<stop stop-color="#F7F1E8"/>',
    '<stop offset=".46" stop-color="#24201C"/>': '<stop offset=".46" stop-color="#EEE5D9"/>',
    '<stop offset="1" stop-color="#100F0E"/>': '<stop offset="1" stop-color="#E6D8CA"/>',
    'id="sage"': 'id="creamGlow"',
    '<stop stop-color="#8F9A77" stop-opacity=".38"/>': '<stop stop-color="#FFFDFC" stop-opacity=".82"/>',
    '<stop offset="1" stop-color="#8FAA77" stop-opacity="0"/>': '<stop offset="1" stop-color="#F8E9DF" stop-opacity="0"/>',
    'fill="url(#sage)"': 'fill="url(#creamGlow)"',
    '<stop stop-color="#FFF8F1" stop-opacity=".105"/>': '<stop stop-color="#FFFFFF" stop-opacity=".72"/>',
    '<stop offset=".42" stop-color="#FFF8F1" stop-opacity=".045"/>': '<stop offset=".42" stop-color="#FFFDFC" stop-opacity=".42"/>',
    '<stop offset="1" stop-color="#D97757" stop-opacity=".075"/>': '<stop offset="1" stop-color="#D97757" stop-opacity=".16"/>',
    '<stop stop-color="#FFF8F1" stop-opacity=".46"/>': '<stop stop-color="#FFFFFF" stop-opacity=".96"/>',
    '<stop offset=".48" stop-color="#FFF8F1" stop-opacity=".10"/>': '<stop offset=".48" stop-color="#FFFFFF" stop-opacity=".42"/>',
    '<stop offset="1" stop-color="#D97757" stop-opacity=".38"/>': '<stop offset="1" stop-color="#D97757" stop-opacity=".66"/>',
    '<stop stop-color="#FFF8F1" stop-opacity=".085"/>': '<stop stop-color="#FFFFFF" stop-opacity=".58"/>',
    '<stop offset=".55" stop-color="#FFF8F1" stop-opacity=".035"/>': '<stop offset=".55" stop-color="#FFFDFC" stop-opacity=".34"/>',
    '<stop offset="1" stop-color="#D97757" stop-opacity=".085"/>': '<stop offset="1" stop-color="#D97757" stop-opacity=".14"/>',
    'flood-color="#000000" flood-opacity=".42"': 'flood-color="#8C6656" flood-opacity=".22"',
    'stroke="#FFF8F1" stroke-width=".7"': 'stroke="#FFFFFF" stroke-width=".7"',
    'stroke="#D97757" stroke-width=".75"': 'stroke="#C96647" stroke-width=".75"',
    'fill="#141210" fill-opacity=".58"': 'fill="#FFFDFC" fill-opacity=".54"',
    'stroke="#FFF8F1" stroke-opacity=".055"': 'stroke="#FFFFFF" stroke-opacity=".72"',
    'fill="#FFF8F1" fill-opacity=".13"': 'fill="#FFFFFF" fill-opacity=".34"',
    'fill="#FFF8F1" fill-opacity=".032"': 'fill="#FFFFFF" fill-opacity=".28"',
    '<circle cx="145" cy="91" r="5.5" fill="#C5D46D"/>': '<circle cx="145" cy="91" r="5.5" fill="#E8A58C"/>',
    '<circle cx="164" cy="91" r="5.5" fill="#8F9A77"/>': '<circle cx="164" cy="91" r="5.5" fill="#2D2926" fill-opacity=".72"/>',
    'fill="#9B8F85"': 'fill="#766B64"',
    'fill="#FFF8F1" fill-opacity=".04" stroke="#FFF8F1" stroke-opacity=".09"': 'fill="#FFFFFF" fill-opacity=".42" stroke="#FFFFFF" stroke-opacity=".78"',
    'fill="#E4A487"': 'fill="#B85C40"',
    'fill="#C7B49E"': 'fill="#6E625B"',
    'fill="#9EA;89"': 'fill="#D97757"',
    'stroke="#FFF8F1" stroke-opacity=".11"': 'stroke="#FFFFFF" stroke-opacity=".84"',
    'stroke="#FFF8F1" stroke-opacity=".13"': 'stroke="#FFFFFF" stroke-opacity=".84"',
    'fill="#9D9188"': 'fill="#8A6558"',
    'animation-delay:70s+': 'animation-delay:70s',
}


def main() -> None:
    svg = SVG_PATH.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        svg = svg.replace(old, new)

    before, remainder = svg.split(START, 1)
    block, after = remainder.split(END, 1)
    groups = re.findall(r'    <g class="quote-container".*?\n    </g>', block, flags=re.DOTALL)
    if len(groups) < 2:
        raise RuntimeError(f"Expected multiple quote groups, found {len(groups)}")

    random.SystemRandom().shuffle(groups)
    refreshed: list[str] = []
    for index, group in enumerate(groups):
        group = re.sub(r'opacity="[01]"', f'opacity="{1 if index == 0 else 0}"', group, count=1)
        group = re.sub(r'animation-delay:\d+s\+?', f'animation-delay:{index * SLOT_SECONDS}s', group, count=1)
        group = re.sub(r'data-quote="\d+"', f'data-quote="{index + 1}"', group, count=1)
        refreshed.append(group)

    updated = before + START + "\n" + "\n".join(refreshed) + "\n    " + END + after
    SVG_PATH.write_text(updated, encoding="utf-8")
    print(f"Applied Claude palette and shuffled {len(refreshed)} quotes.")


if __name__ == "__main__":
    main()
