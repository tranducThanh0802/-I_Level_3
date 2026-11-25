# Agent Team — khung hỗ trợ quy trình phát triển app

Bộ khung (cấu hình + bộ nhớ + script) cho một **agent team** chạy trong Claude Code. Quy trình con người không đổi: người giao spec, người
duyệt và merge, người phát hành store. Agent làm các bước máy kiểm được (đọc, sửa, build/test, mở PR) và để lại log.

## Dùng khung cho project mới
```bash
python3 scripts/init_project.py ~/Projects/MyApp "MyApp Android"   # copy agent-team/ + scripts/ + CLAUDE.md, KHÔNG copy bí mật
cd ~/Projects/MyApp && python3 scripts/build_board.py              # sinh dashboard
```
Rồi điền `agent-team/memory/project-knowledge.md` (kiến trúc, lệnh build, quyết định cũ) — **chưa điền thì chưa chạy agent**.

## Đọc theo thứ tự (cũng là giao thức mở context mới)
1. `agent-team/STATE.md` — đang ở đâu · 2. `CLAUDE.md` + `agent-team/memory/core-rules.md` — luật · 3. `agent-team/workspace/` — việc dở
4. `agent-team/memory/bugs/` — bug đã gặp · 5. `agent-team/DECISIONS.md` — vì sao quyết thế.

## Các lệnh chính
| Việc | Lệnh |
|---|---|
| Báo cáo dùng thật + tỷ lệ tự động hoá (từ log) | `python3 scripts/usage_report.py` |
| Báo cáo §6 (tiết kiệm thời gian người) | `python3 scripts/build_report.py` |
| Chạy bộ hồi quy 20 tình huống | `python3 scripts/run_regression.py` |
| Quét secret/PII trước commit | `python3 scripts/scan_secrets.py --install-hook` |
| Gợi ý cải thiện từ lỗi lặp (loop ngoài) | `python3 scripts/outer_loop.py` |

## Luật không bao giờ nới (chi tiết: `agent-team/memory/core-rules.md`)
Agent không merge, không đẩy store · danh sách phải-dừng-hỏi · "xong" phải máy kiểm được · bàn giao đủ code + video + ảnh trước/sau.
Ngoại lệ có chủ đích nào cũng phải có ADR trong `DECISIONS.md`.

## Phiên bản
`VERSION` và `CHANGELOG.md` (mỗi phiên bản có mục tiêu và thời hạn).
