#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Báo cáo TIẾN ĐỘ ra Excel: bao-cao-tien-do.xlsx
Đã làm gì / còn thiếu gì / % — theo khung đề bài. Sửa nội dung ở list ROWS bên dưới khi có tiến triển.
Chạy: python3 scripts/build_status_excel.py
"""
import os, json, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "bao-cao-tien-do.xlsx")
try:
    PROJECT = json.load(open(os.path.join(ROOT, "project.config.json"), encoding="utf-8")).get("name", "Agent Team")
except Exception:
    PROJECT = "Agent Team"

# Hạng mục | trạng thái(green/yellow/red) | % | Đã làm | Còn thiếu
ROWS = [
    ("Soát spec", "yellow", 40, "Luật + rubric + specs gating (draft→approved)", "Chưa có agent chạy thật; chưa đối chiếu spec↔docs BE"),
    ("Dev", "yellow", 35, "Guide + isolation (worktree) + luật cấm-tự-quyết", "Chưa có agent chạy ra PR; video chưa verify"),
    ("Fix bug", "yellow", 55, "Guide 2-mode + bug DB (khóa/đếm/nhãn) + bug board", "Chưa có skill chạy thật; chưa e2e tới PR"),
    ("Test", "yellow", 40, "Rubric + luật phủ 4 trạng thái + kết quả máy thật", "Chưa tách phase chạy; chưa chạy thật"),
    ("Luồng feature", "yellow", 40, "Flow + pipeline spec-drafter→soát→dev→test", "Chưa chạy e2e"),
    ("Luồng fix bug", "yellow", 50, "Flow + bug board 'Cần người' + Discord", "Chưa chạy 1 bug thật tới merge; chưa nối Jira/CI"),
    ("Không nới quyền (merge/store)", "green", 100, "Chỉ tạo PR nháp; luật lõi ghi rõ; hook chặn", "—"),
    ("Bộ nhớ 5 tầng", "green", 85, "Đủ 5 tầng; agent chỉ ghi 2 chỗ; trong repo", "Thiếu dọn định kỳ; chưa test tra-lại thật"),
    ("Loop trong + giữa", "yellow", 60, "Thiết kế máy-kiểm + 3 chặn vô hạn + STATE resume", "Chưa chạy thật"),
    ("Loop ngoài", "green", 80, "outer_loop.py (lỗi lặp≥3) + cổng regression + docs", "Chưa có data sửa-tay thật để kích hoạt"),
    ("Bộ tình huống hồi quy", "yellow", 50, "10 tình huống + baseline + cổng chặn (test qua/chặn)", "Cần góp đủ 20 từ việc thật + results thật"),
    ("Đo lường / báo cáo", "green", 85, "Web + Excel; median; tách chờ ngoài; gộp-trùng; bug-quay-lại", "Số hiện là DEMO — cần số thật"),
    ("Hệ quản lý (web + Discord)", "green", 90, "5 web (dashboard/board/bugboard/report/exchanges) + Discord màu", "—"),
    ("Nhân bản per-project", "green", 90, "init_project.py + project.config + cô lập dữ liệu", "—"),
    ("Đủ mẫu thật (≥5/loại)", "red", 5, "Hạ tầng đo đủ", "Mới toàn DEMO — 0 việc thật"),
    ("Agent chạy thật (e2e)", "red", 5, "Có guide + kế hoạch tuần 1", "Chưa wire .claude/agents + hook vào repo iOS thật"),
]

STY = {"green": ("C6EFCE", "006100", "🟢 Đã làm"),
       "yellow": ("FFEB9C", "9C6500", "🟡 Một phần"),
       "red": ("FFC7CE", "9C0006", "🔴 Chưa làm")}

overall = round(sum(r[2] for r in ROWS) / len(ROWS))
frame_rows = [r for r in ROWS if r[0] not in ("Đủ mẫu thật (≥5/loại)", "Agent chạy thật (e2e)")]
frame = round(sum(r[2] for r in frame_rows) / len(frame_rows))
exec_rows = [r for r in ROWS if r[0] in ("Đủ mẫu thật (≥5/loại)", "Agent chạy thật (e2e)", "Lo", )]
exec_pct = 10

HEAD = Font(bold=True, color="FFFFFF"); HFILL = PatternFill("solid", fgColor="2F6FEB")
THIN = Border(*[Side(style="thin", color="DDDDDD")] * 4)
wrap = Alignment(wrap_text=True, vertical="top")

wb = Workbook(); ws = wb.active; ws.title = "Tiến độ"

ws["A1"] = f"{PROJECT} — Báo cáo tiến độ"; ws["A1"].font = Font(bold=True, size=15)
ws["A2"] = f"Cập nhật: {datetime.date.today().isoformat()}"; ws["A2"].font = Font(italic=True, color="808080")

# tóm tắt
ws["A4"] = "Tổng tiến độ"; ws["B4"] = f"{overall}%"
ws["A5"] = "Khung & công cụ"; ws["B5"] = f"{frame}%"
ws["A6"] = "Vận hành thật (e2e)"; ws["B6"] = f"~{exec_pct}%"
ws["A7"] = "Bậc hiện tại"; ws["B7"] = "Bậc 1 (thiết kế xong, chưa chạy thật) → mầm Bậc 2"
ws["A8"] = "Ưu tiên tiếp"; ws["B8"] = "1) Wire agent chạy thật vào repo iOS  2) Chạy e2e lấy số thật  3) Góp đủ 20 tình huống"
for r in range(4, 9):
    ws[f"A{r}"].font = Font(bold=True)
    ws[f"B{r}"].alignment = wrap
ws["B4"].font = Font(bold=True, size=13, color="2F6FEB")

# bảng
hr = 10
headers = ["Hạng mục", "Trạng thái", "%", "Đã làm được", "Còn thiếu"]
for i, h in enumerate(headers, 1):
    c = ws.cell(row=hr, column=i, value=h); c.font = HEAD; c.fill = HFILL
for j, (name, st, pct, done, miss) in enumerate(ROWS):
    r = hr + 1 + j
    fill, fontc, label = STY[st]
    ws.cell(row=r, column=1, value=name).font = Font(bold=True)
    cst = ws.cell(row=r, column=2, value=label)
    cst.fill = PatternFill("solid", fgColor=fill); cst.font = Font(color=fontc, bold=True)
    ws.cell(row=r, column=3, value=pct / 100).number_format = "0%"
    ws.cell(row=r, column=4, value=done).alignment = wrap
    ws.cell(row=r, column=5, value=miss).alignment = wrap
    for col in range(1, 6):
        ws.cell(row=r, column=col).border = THIN

for i, w in enumerate([30, 14, 7, 48, 48], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = f"A{hr+1}"

wb.save(OUT)
print(f"Đã tạo: {OUT}  | Tổng {overall}% (khung {frame}%, vận hành ~{exec_pct}%)")
