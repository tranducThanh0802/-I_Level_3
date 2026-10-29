# Danh mục ĐẦU VIỆC LẶP của công ty agent (A6)

> "Khai danh mục đầu việc lặp → tự động hoá ≥80%, chứng minh bằng LOG chứ không bằng lời" (rubric A6).
> Mỗi việc: tần suất · đã auto chưa (script) · nhánh ngoại lệ. `% auto` = việc auto hoàn toàn / tổng.

| # | Đầu việc lặp | Tần suất | Auto? | Bằng (script/lệnh) | Nhánh ngoại lệ |
|---|--------------|----------|-------|--------------------|----------------|
| 1 | Soát sức khoẻ công ty skill | mỗi lần thêm skill / trước giao | ✅ | `health_check.py` | thiếu file → báo rõ, không crash |
| 2 | Cổng QA icon/emoji | mỗi commit | ✅ | `ui_lint.py` (pre-commit) | `// lint:allow-emoji` cho share-text |
| 3 | Cổng nghiệm thu "xong" | mỗi feature | ✅ | `acceptance_gate.py` | 📋 out_of_scope |
| 4 | Quét secret/PII | mỗi commit | ✅ | `scan_secrets.py` (pre-commit) | phát hiện → chặn, hỏi CEO |
| 5 | Hồi quy không tụt baseline | mỗi lần đổi luật | ✅ | `run_regression.py` | tụt → chặn |
| 6 | Dựng project mới từ template | mỗi project | ✅ | `init_project.py` | — |
| 7 | Sinh báo cáo tiến độ | định kỳ | ✅ | `build_report*.py` | — |
| 8 | Nạp/lấy việc hàng đợi | hằng ngày | ✅ | `work_queue.py` | — |
| 9 | Ghi run-log | mỗi lần chạy | ✅ | `agent_cli.py log` | — |
| 10 | Thêm skill mới vào org | khi mở rộng | ✅ | `agent_cli.py new-skill` | nhắc thêm vào DEPT |
| 11 | Chạy trọn cổng trước giao | mỗi feature | ✅ | `agent_cli.py check` (gộp 1,2,3) | — |
| 12 | Retro sau feature | mỗi feature | ⚠️ bán-auto | `feature-retro` (người + agent) | **cố ý người** — cần phán đoán |
| 13 | Review độc lập (verdict) | mỗi feature | ⚠️ bán-auto | `independent-review` (spawn agent; **người/agent khác quyết**) | **cố ý người** — A4 |

## Đầu việc lặp THẬT trên sản phẩm (Lingora iOS — "việc thật" của CEO)
> Đây mới là nguồn bằng chứng A3 chính (không phải việc meta framework ở trên). Log: `runs.jsonl` (`product=Lingora iOS`).

| Đầu việc lặp | Tần suất phiên này | Phần AI làm | Phần auto/máy-chặn | Người (CEO) |
|---|---|---|---|---|
| **ui-parity-fix** (sửa UI khớp Android) | nhiều (champion, icon, leaderboard, lesson, WotD) | dò lệch + code sửa | `ui_lint` auto bắt cả LỚP icon/emoji; acceptance-gate | duyệt "đẹp"/đồng ý |
| **bugfix** (crash/report) | video crash… | tra nguyên nhân + sửa + test | build/test xanh; bug-memory | duyệt |
| **logic-parity** (khớp số/luật Android) | lock lesson, XP… | port logic | `port-oracle-tests` (test Android làm oracle) | duyệt |

→ 6 run Lingora THẬT đã log phiên này; 4 qua gate máy, 2 qua review độc lập (WotD, lock). Việc LẶP được chặn bằng MÁY
(ui_lint bắt mọi icon-tofu, acceptance-gate chặn "xong" non) → đúng tinh thần A6 "auto phần lặp của việc".

## Tỷ lệ tự động hoá
- Tổng việc lặp khai: **13**
- Auto hoàn toàn: **11** → **~85%** (≥80% → đạt mốc A6 ≥3).
- 2 việc còn lại (12,13) **cố ý giữ người-trong-vòng** (retro cần phán đoán; verdict review là quyết định A4) — KHÔNG phải chưa làm được, mà là KHÔNG NÊN auto hoàn toàn.
- Hướng mốc 5 ("loại bỏ việc lặp thay vì chỉ auto"): `agent check` **gộp** 3 việc (health+lint+acceptance) thành 1 lệnh → giảm số thao tác lặp, không chỉ auto từng cái.

## Bằng chứng (không bằng lời)
- `agent-team/logs/runs.jsonl` — mỗi lần chạy 1 dòng (`repeat_task` để đếm tần suất từng việc).
- ⚠️ Nhiều run đang `baseline_source=agent-estimated` → CHƯA tính "tiết kiệm ≥40%" (§6). **CEO đặt baseline (human)** cho từng đầu việc để số liệu hợp lệ.
