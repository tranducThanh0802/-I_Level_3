#!/bin/sh
# Cài git pre-commit hook (scan_secrets + ui_lint) cho repo. .git/hooks không theo git nên mỗi clone chạy 1 lần.
ROOT="$(git rev-parse --show-toplevel)"
HOOK="$ROOT/.git/hooks/pre-commit"
cat > "$HOOK" <<'EOF'
#!/bin/sh
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 1
[ -f scripts/scan_secrets.py ] && { python3 scripts/scan_secrets.py || { echo '⛔ secret'; exit 1; }; }
[ -f scripts/ui_lint.py ] && { python3 scripts/ui_lint.py --quiet || { echo '⛔ ui_lint'; exit 1; }; }
EOF
chmod +x "$HOOK"
echo "Đã cài pre-commit hook → $HOOK"
