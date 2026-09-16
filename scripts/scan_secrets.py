#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cổng quét SECRET + PII trước khi commit / gửi Discord (lỗ hổng #4).
- SECRET (khóa API, private key, token, webhook...) -> CHẶN (exit 1).
- PII (email, số điện thoại) -> CẢNH BÁO (exit 0; --strict thì cũng chặn).

Dùng:
  python3 scripts/scan_secrets.py            # quét file đang staged (git)
  python3 scripts/scan_secrets.py --all      # quét toàn bộ file tracked
  python3 scripts/scan_secrets.py f1 f2 ...   # quét file chỉ định
  python3 scripts/scan_secrets.py --install-hook   # cài pre-commit hook tự chặn
"""
import os, re, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRETS = [
    ("Private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("Slack/Discord webhook", re.compile(r"https://(hooks\.slack\.com|discord(app)?\.com/api/webhooks)/\S+")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("Khóa gán biến (key/secret/token/password = '...')",
     re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key)\b\s*[:=]\s*['\"][^'\"]{16,}['\"]")),
]
PII = [
    ("Email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("SĐT VN", re.compile(r"(?<!\d)(0|\+84)\d{9}(?!\d)")),
]
# đuôi file nhạy cảm không nên commit
BAD_EXT = (".p12", ".mobileprovision", ".cer", ".pem", ".keystore", ".jks", ".env")
SKIP_DIR = ("/.git/", "/node_modules/", "/.build/", "/DerivedData/")
SKIP_FILE = ("scan_secrets.py",)  # tránh tự báo chính regex của mình


def is_text(path):
    try:
        with open(path, "rb") as f:
            return b"\x00" not in f.read(2048)
    except Exception:
        return False


def target_files():
    if len(sys.argv) > 1 and sys.argv[1] not in ("--all", "--strict", "--install-hook"):
        return [a for a in sys.argv[1:] if not a.startswith("--")]
    try:
        if "--all" in sys.argv:
            out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
        else:
            out = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True)
        return [os.path.join(ROOT, p) for p in out.splitlines() if p.strip()]
    except Exception:
        return []


def install_hook():
    hook = os.path.join(ROOT, ".git", "hooks", "pre-commit")
    if not os.path.isdir(os.path.dirname(hook)):
        print("Không thấy .git/hooks — repo đã init chưa?"); return
    with open(hook, "w") as f:
        f.write("#!/bin/sh\npython3 scripts/scan_secrets.py || {\n"
                "  echo 'Commit bị chặn: phát hiện secret. Sửa rồi commit lại (hoặc git commit --no-verify nếu chắc chắn an toàn).'\n"
                "  exit 1\n}\n")
    os.chmod(hook, 0o755)
    print(f"✅ Đã cài pre-commit hook: {hook}\n   Từ giờ mỗi lần commit sẽ tự quét secret.")


def main():
    if "--install-hook" in sys.argv:
        install_hook(); return
    strict = "--strict" in sys.argv
    files = target_files()
    secret_hits, pii_hits, badext = [], [], []
    for path in files:
        if any(s in path.replace("\\", "/") for s in SKIP_DIR) or os.path.basename(path) in SKIP_FILE:
            continue
        if path.lower().endswith(BAD_EXT):
            badext.append(path); continue
        if not os.path.isfile(path) or not is_text(path):
            continue
        try:
            lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
        except Exception:
            continue
        for i, ln in enumerate(lines, 1):
            for name, rx in SECRETS:
                if rx.search(ln):
                    secret_hits.append((path, i, name))
            for name, rx in PII:
                if rx.search(ln):
                    pii_hits.append((path, i, name))

    rel = lambda p: os.path.relpath(p, ROOT)
    if badext:
        for p in badext:
            secret_hits.append((p, 0, "File nhạy cảm (không nên commit)"))
    if secret_hits:
        print("⛔ SECRET phát hiện (CHẶN):")
        for p, i, n in secret_hits:
            print(f"  - {rel(p)}:{i} — {n}")
    if pii_hits:
        print(f"⚠️  PII phát hiện ({len(pii_hits)}) — cân nhắc, đặc biệt trước khi gửi Discord:")
        for p, i, n in pii_hits[:20]:
            print(f"  - {rel(p)}:{i} — {n}")
        if len(pii_hits) > 20:
            print(f"  ... và {len(pii_hits)-20} chỗ nữa")

    if secret_hits or (strict and pii_hits):
        print("\n=> CHẶN. Gỡ secret (đưa vào biến môi trường / file .gitignore) rồi thử lại.")
        sys.exit(1)
    if not secret_hits and not pii_hits:
        print(f"✅ Sạch — không thấy secret/PII trong {len(files)} file.")
    else:
        print("\n✅ Không có SECRET (chỉ có cảnh báo PII). Cho qua.")


if __name__ == "__main__":
    main()
