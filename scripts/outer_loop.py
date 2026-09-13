#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loop NGOÀI (§4 đề bài, tầng ngoài): gom các lần SỬA TAY từ logs → tìm lỗi lặp ≥3 lần
→ đề xuất cập nhật cẩm nang. CHỈ đề xuất, KHÔNG tự sửa (người duyệt + chạy run_regression trước khi áp).

Chạy: python3 scripts/outer_loop.py
Xuất ra màn hình + ghi agent-team/outer-loop-proposals.md
"""
import os, re, json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AT = os.path.join(ROOT, "agent-team")
THRESHOLD = 3  # đề bài: chỉ sửa cẩm nang khi một lỗi đã lặp ≥3 lần
OUT = os.path.join(AT, "outer-loop-proposals.md")

# gợi ý loại sửa tay -> cẩm nang/chuẩn liên quan
HINT = {
    "sai chuẩn": "memory/project-knowledge.md (chuẩn code) hoặc memory/playbooks/",
    "thiếu thông tin đầu vào": "specs/ (tiêu chí nghiệm thu) + con Soát spec",
    "hiểu sai yêu cầu": "memory/playbooks/ (ví dụ đúng/sai) + con Soát spec",
    "sai logic": "memory/playbooks/ của loại việc + review",
}


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def main():
    rp = os.path.join(AT, "logs", "runs.jsonl")
    fixes = []
    if os.path.exists(rp):
        for line in open(rp, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            for mf in r.get("manual_fixes", []):
                fixes.append((norm(mf.get("type", "?")), norm(mf.get("detail", ""))))

    by_type = Counter(t for t, _ in fixes)
    by_issue = Counter(fixes)  # (type, detail) cụ thể

    proposals = [(k, c) for k, c in by_issue.items() if c >= THRESHOLD]
    proposals.sort(key=lambda x: -x[1])

    lines = ["# Đề xuất loop ngoài (tự sinh — CHỈ đề xuất, người duyệt)\n",
             f"> Ngưỡng: lỗi lặp ≥{THRESHOLD} lần mới đề xuất sửa cẩm nang (đề bài §4). "
             f"Tổng lần sửa tay đã ghi: **{len(fixes)}**.\n",
             "> Quy trình áp: người duyệt → sửa cẩm nang → `python3 scripts/run_regression.py` "
             "(không tụt baseline) → cập nhật baseline.\n",
             "## Tổng theo loại sửa tay"]
    if by_type:
        for t, c in by_type.most_common():
            lines.append(f"- {t}: {c} lần")
    else:
        lines.append("- (chưa có lần sửa tay nào được ghi)")

    lines.append("\n## Đề xuất cập nhật cẩm nang (lỗi lặp ≥3)")
    if proposals:
        for (t, d), c in proposals:
            lines.append(f"- **[{c} lần] loại: {t}** — \"{d}\"\n"
                         f"    → xem xét sửa: {HINT.get(t, 'memory/playbooks/')}  · trạng thái: **chờ người duyệt**")
    else:
        lines.append(f"- Chưa có lỗi nào lặp ≥{THRESHOLD} lần. Chưa cần sửa cẩm nang "
                     "(nhét ngoại lệ 1–2 lần vào cẩm nang sẽ làm nó phình & tự mâu thuẫn — đề bài §4).")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"(Đã ghi {OUT})")


if __name__ == "__main__":
    main()
