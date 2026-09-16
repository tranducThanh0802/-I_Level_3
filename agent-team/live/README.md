# Live — theo dõi agent chạy TRỰC TIẾP

> `activity.jsonl` = dòng sự kiện tiến trình agent phát ra khi đang chạy (mỗi bước một dòng).
> File này EPHEMERAL (đã .gitignore) — là feed live, không phải hồ sơ. Hồ sơ chính thức = `logs/runs.jsonl`.

## 3 tầng theo dõi
| Tầng | Khi nào | Cách |
|---|---|---|
| **Live** (đang chạy) | agent đang làm | `python3 scripts/watch_live.py` (terminal) · Discord phòng agent (điện thoại) |
| Ảnh chụp | tổng quan | dashboard/board/report (refresh) |
| Hồi cứu | sau khi xong | `logs/runs.jsonl` + report + exchanges |

## Agent phát sự kiện thế nào
Mỗi khi qua một bước, agent gọi:
```
python3 scripts/emit_activity.py --agent fixbug --task BUG-5 --step "tìm nguyên nhân gốc" --status running [--discord]
```
`status`: running | done | blocked | failed.

## Người xem thế nào
```
python3 scripts/watch_live.py        # theo dõi realtime (Ctrl+C thoát)
python3 scripts/watch_live.py --once # trạng thái hiện tại rồi thoát
```
Hoặc mở Discord (nếu agent phát kèm `--discord`) → thấy trên điện thoại.

## Định dạng dòng
```json
{"ts":"2026-09-16T22:05:12","agent":"fixbug","task":"BUG-5","step":"chạy test","status":"done","note":""}
```
