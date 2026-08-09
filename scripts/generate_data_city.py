#!/usr/bin/env python3
"""Generate a dark isometric language skyline from public GitHub data."""

from __future__ import annotations

import json
import os
import urllib.request
from collections import defaultdict
from pathlib import Path


USER = os.getenv("GITHUB_USER", "guivital1")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUTPUT = Path(os.getenv("OUTPUT_PATH", "assets/data-city.svg"))
COLORS = ["#a6e22e", "#7dd3fc", "#c4b5fd", "#f9a8d4", "#fbbf24", "#94a3b8"]


def github(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-data-city"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def collect():
    repos = github(f"/users/{USER}/repos?per_page=100&type=owner&sort=updated")
    totals = defaultdict(int)
    included = []
    for repo in repos:
        if repo["fork"] or repo["archived"]:
            continue
        included.append(repo)
        try:
            for language, size in github(repo["languages_url"].removeprefix("https://api.github.com")).items():
                totals[language] += size
        except Exception:
            continue
    return included, sorted(totals.items(), key=lambda item: item[1], reverse=True)[:6]


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def short_label(value: str) -> str:
    return {"Jupyter Notebook": "Jupyter", "TypeScript": "TypeScript"}.get(value, value[:12])


def polygon(points, fill, opacity=1):
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{coords}" fill="{fill}" opacity="{opacity}"/>'


def render(repo_count, languages):
    width, height = 920, 360
    maximum = max((size for _, size in languages), default=1)
    chunks = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<title>{esc(USER)} data city</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b0f10"/><stop offset="1" stop-color="#111718"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="920" height="360" rx="18" fill="url(#bg)"/>
<g stroke="#263032" stroke-width="1" opacity=".65">''']
    for y in range(230, 341, 22):
        chunks.append(f'<path d="M70 {y} L460 {y-105} L850 {y}" fill="none"/>')
    for x in range(70, 851, 65):
        chunks.append(f'<path d="M{x} 340 L460 235" fill="none"/>')
    chunks.append('</g><text x="54" y="55" fill="#f4f4f0" font-family="ui-monospace,monospace" font-size="22" font-weight="700">DATA CITY</text>')
    chunks.append('<circle cx="805" cy="49" r="4" fill="#a6e22e" filter="url(#glow)"><animate attributeName="opacity" values=".35;1;.35" dur="2.4s" repeatCount="indefinite"/></circle>')
    chunks.append('<text x="820" y="54" fill="#839092" font-family="ui-monospace,monospace" font-size="12">LIVE DATA</text>')

    for index, (language, size) in enumerate(languages):
        col, row = index % 3, index // 3
        x = 190 + col * 205 + row * 52
        base = 294 - row * 56
        building_height = 44 + (size / maximum) * 120
        w, depth = 74, 30
        top = base - building_height
        color = COLORS[index % len(COLORS)]
        chunks.append('<g>')
        chunks.append(polygon([(x, top), (x+w, top-depth), (x+w, base-depth), (x, base)], color, .72))
        chunks.append(polygon([(x+w, top-depth), (x+w+depth, top), (x+w+depth, base), (x+w, base-depth)], color, .38))
        chunks.append(polygon([(x, top), (x+depth, top+depth), (x+w+depth, top), (x+w, top-depth)], color, .96))
        chunks.append(f'<text x="{x+8}" y="{base+22}" fill="#d9dfdc" font-family="ui-monospace,monospace" font-size="12">{esc(short_label(language))}</text>')
        percent = size / sum(value for _, value in languages) * 100
        percent_label = "&lt;0.1%" if 0 < percent < 0.1 else f"{percent:.1f}%"
        chunks.append(f'<text x="{x+8}" y="{base+38}" fill="#738083" font-family="ui-monospace,monospace" font-size="10">{percent_label}</text></g>')

    if not languages:
        chunks.append('<text x="460" y="195" text-anchor="middle" fill="#839092" font-family="ui-monospace,monospace" font-size="14">Waiting for repository data…</text>')
    chunks.append(f'<text x="54" y="325" fill="#839092" font-family="ui-monospace,monospace" font-size="12">{repo_count} ORIGINAL REPOS  ·  {len(languages)} TOP LANGUAGES  ·  @{esc(USER)}</text>')
    chunks.append('</svg>')
    return "".join(chunks)


def main():
    repos, languages = collect()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(len(repos), languages), encoding="utf-8")


if __name__ == "__main__":
    main()
