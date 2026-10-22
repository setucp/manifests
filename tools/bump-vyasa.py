#!/usr/bin/env python3
"""Point vyasa/manifest.toml at a Vyasa release.

    tools/bump-vyasa.py 0.3.4

Downloads both Linux archives, computes their sha256 from the bytes (never
from a published checksum), and rewrites version, URLs, sha256 and exec
paths. Prints the old version, or nothing when already current.
"""
import hashlib
import re
import sys
import urllib.request

MANIFEST = "vyasa/manifest.toml"
BASE = "https://github.com/vyasa-cms/vyasa/releases/download"
ARCHES = ("x86_64", "aarch64")


def sha256_of(url: str) -> str:
    h = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=300) as r:
        for chunk in iter(lambda: r.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    new = sys.argv[1].lstrip("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+", new):
        raise SystemExit(f"not a release version: {new}")
    text = open(MANIFEST).read()
    m = re.search(r'^version = "([^"]+)"', text, re.M)
    if not m:
        raise SystemExit("manifest has no version line")
    old = m.group(1)
    if old == new:
        return 0
    for arch in ARCHES:
        name = f"vyasa-{new}-{arch}-unknown-linux-gnu.tar.gz"
        digest = sha256_of(f"{BASE}/v{new}/{name}")
        pattern = rf'(vyasa-{re.escape(old)}-{arch}-unknown-linux-gnu\.tar\.gz"\s*\nsha256 = ")[0-9a-f]{{64}}'
        text, n = re.subn(pattern, rf"\g<1>{digest}", text)
        if n != 1:
            raise SystemExit(f"no {arch} entry for {old} in {MANIFEST}")
    text = text.replace(old, new)
    open(MANIFEST, "w").write(text)
    print(old)
    return 0


if __name__ == "__main__":
    sys.exit(main())
