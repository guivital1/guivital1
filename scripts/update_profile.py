from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

OWNER = os.getenv("PROFILE_OWNER", "guivital1")
PROFILE_REPO = os.getenv("PROFILE_REPO", f"{OWNER}/{OWNER}")
README_PATH = os.getenv("README_PATH", "README.md")
TOKEN = os.getenv("GITHUB_TOKEN", "")
API = "https://api.github.com"

DATA_KEYWORDS = {
    "analytics",
    "analysis",
    "data",
    "dados",
    "python",
    "sql",
    "machine-learning",
    "ml",
    "etl",
    "pipeline",
    "bi",
    "science",
    "statistics",
}

ARCHIVE_NAMES = {
    "hospital-crm-analytics",
    "cartola-data-analysis",
    "sampling-methods-lab",
    "movimenta-optimization",
}


def request_json(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "guivital1-profile-automation",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def list_public_repos() -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"{API}/users/{OWNER}/repos?per_page=100&page={page}&sort=created&direction=desc"
        batch = request_json(url)
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos


def is_data_repo(repo: dict[str, Any]) -> bool:
    if repo.get("archived") or repo.get("fork") or repo.get("private"):
        return False
    name = repo.get("name", "")
    if name == OWNER or name in ARCHIVE_NAMES:
        return False
    haystack = " ".join(
        str(repo.get(key) or "")
        for key in ("name", "description", "language")
    ).lower().replace("_", "-")
    topics = " ".join(repo.get("topics") or []).lower()
    return any(keyword in haystack or keyword in topics for keyword in DATA_KEYWORDS)


def repo_line(repo: dict[str, Any]) -> str:
    name = repo["name"]
    description = (repo.get("description") or "new data project").strip()
    updated = repo.get("updated_at", "")[:10]
    return f'<a href="https://github.com/{OWNER}/{name}"><code>{name}</code></a> <sub>{description} · updated {updated}</sub>'


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    if start not in text or end not in text:
        raise ValueError(f"Missing marker pair: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{replacement}\n{end}{after}"


def build_radar(repos: list[dict[str, Any]]) -> str:
    fresh_data = [repo for repo in repos if is_data_repo(repo)][:3]
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not fresh_data:
        return (
            f'<p align="center"><sub>Profile checked {checked_at} · old projects preserved · '
            'waiting for the next data build.</sub></p>'
        )
    rows = "<br/>\n".join(repo_line(repo) for repo in fresh_data)
    return (
        f'<p align="center"><sub>Profile checked {checked_at} · latest data-oriented repos</sub><br/>\n'
        f'{rows}</p>'
    )


def fetch_readme() -> dict[str, Any]:
    return request_json(f"{API}/repos/{PROFILE_REPO}/contents/{README_PATH}")


def update_readme(readme: dict[str, Any], content: str) -> None:
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    request_json(
        f"{API}/repos/{PROFILE_REPO}/contents/{README_PATH}",
        method="PUT",
        payload={
            "message": "Update automated profile radar",
            "content": encoded,
            "sha": readme["sha"],
        },
    )


def main() -> int:
    repos = list_public_repos()
    readme = fetch_readme()
    current = base64.b64decode(readme["content"]).decode("utf-8")
    updated = replace_between(
        current,
        "<!-- portfolio-radar:start -->",
        "<!-- portfolio-radar:end -->",
        build_radar(repos),
    )
    if updated == current:
        print("README already up to date.")
        return 0
    update_readme(readme, updated)
    print("README profile radar updated.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"), file=sys.stderr)
        raise
