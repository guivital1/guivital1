from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

README = Path(os.getenv("README_PATH", "README.md"))
TIMEOUT = 20

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=\"([^\"]+)\"")


def extract_targets(text: str) -> list[str]:
    targets = set(MARKDOWN_LINK_RE.findall(text))
    targets.update(HTML_LINK_RE.findall(text))
    return sorted(target for target in targets if not target.startswith("#"))


def check_local(path: str) -> str | None:
    clean = path.split("?", 1)[0]
    if Path(clean).exists():
        return None
    return f"missing local file: {path}"


def check_url(url: str) -> str | None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "guivital1-profile-link-checker"},
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if response.status < 400:
                return None
            return f"HTTP {response.status}: {url}"
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 405}:
            get_request = urllib.request.Request(
                url,
                headers={"User-Agent": "guivital1-profile-link-checker"},
                method="GET",
            )
            try:
                with urllib.request.urlopen(get_request, timeout=TIMEOUT) as response:
                    return None if response.status < 400 else f"HTTP {response.status}: {url}"
            except Exception as get_exc:  # noqa: BLE001
                return f"{type(get_exc).__name__}: {url}"
        return f"HTTP {exc.code}: {url}"
    except Exception as exc:  # noqa: BLE001
        return f"{type(exc).__name__}: {url}"


def main() -> int:
    text = README.read_text(encoding="utf-8")
    failures: list[str] = []
    for target in extract_targets(text):
        if target.startswith(("http://", "https://")):
            failure = check_url(target)
        else:
            failure = check_local(target)
        if failure:
            failures.append(failure)

    if failures:
        print("Profile link check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Profile links and images look healthy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
