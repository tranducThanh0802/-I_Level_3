# RUBRIC-MAP — tiêu chí đánh giá ↔ skill/script ↔ bằng chứng

> Mỗi tiêu chí trong đề chấm được phủ bởi skill/script nào + chứng minh bằng gì (máy, không bằng lời).
> Dùng `python3 scripts/agent_cli.py rubric` để in trạng thái tự động.

## LỚP 1 (Must)

| Mã | Tiêu chí | Phủ bởi | Bằng chứng ĐẠT |
|----|----------|---------|-----------------|
| **A8** | Hệ thống, hình hài hoàn chỉnh | CLI `scripts/agent_cli.py` + `.claude/skills/*` + `scripts/init_project.py` | Người khác `git clone` + `init_project.py` → chạy lại được (không chỉ máy mình) |
| A8.1 | Đóng gói, move, tái sử dụng cá nhân | Skills chuẩn SKILL.md + CLI | Copy `.claude/skills/` sang project khác → dùng ngay |
| A8.2 | Hình hài: web/desktop/plugin/bot/**CLI** | CLI `agent` (chọn làm trước) | `agent_cli.py --help` liệt kê lệnh; chạy workflow + gate qua CLI |
| **A4** | Người duyệt gợi ý & quyết tại checkpoint | `core-rules §1/§4` + `make-acceptance` + `acceptance-gate` + `independent-review` | Workflow có điểm dừng THẬT; khi dừng báo ngay + 2 phương án; gate chặn nếu thiếu người duyệt |
| A4.1 | Chỉ dừng ở điểm người phải làm | `core-rules §1` (danh sách cấm-tự-quyết) | Điểm dừng = tiền/đăng nhập/dữ liệu user/kiến trúc… (có lý do), không dừng vô cớ |
| A4.2 | Biết tạo điểm chặn | `acceptance-gate` + `ui-lint` + `regression-gate` | Gate máy exit 1 khi chưa đủ → chặn commit/"xong" |
| A5 | Độ khó theo bộ phận (Hội đồng ra đề) | `core-rules` + CEO ra đề | Ngoài tầm skill — do người/hội đồng |

## LỚP 2 (chấm 1–5) — mục tiêu ≥3, hướng 4–5

| Mã | Tiêu chí (trọng số) | Phủ bởi | Mốc 3 (ĐẠT) | Hướng 4–5 |
|----|---------------------|---------|-------------|-----------|
| **A1** (1) | Workflow auto 2–3 bước nối | `orchestrate` + `write-spec`(A1.1) | Quy trình rõ, đánh dấu phần AI, nối 2–3 bước chạy trọn | ≥4 bước + nhánh ngoại lệ; chuẩn hoá mẫu |
| **A2** (2) | Knowledge Base + loop liên tục | `knowledge-base` + `outer-loop` + `bug-memory` | KB = tập quy tắc rõ, biết dùng ở bước nào, đã sửa vài lần | Nhịp cập nhật xác định + version + tiêu chí loại quy tắc cũ; chứng minh đầu ra tốt lên |
| **A3** (2) | Đóng góp trực tiếp + log | `run-log` + `work-queue` | Có log, dùng đều trên dữ liệu thật, đạt tần suất tối thiểu | Gần như lần nào phát sinh cũng dùng + đo thời gian tiết kiệm; nhóm cùng dùng |
| **A6** (2) | Auto 80% việc lặp | `automate-repeat` + các gate | ≥80% danh mục đã khai, chứng minh bằng log | Có nhánh ngoại lệ; loại bỏ việc lặp thay vì chỉ auto |

## LỚP 3

| Mã | Tiêu chí | Phủ bởi | Ghi chú |
|----|----------|---------|---------|
| A7 | Bản sao 1:1 online của CEO qua AI | `my-replica` (điểm cộng) | Làm sau khi Lớp 1–2 vững |

## Hiện trạng (cập nhật khi tiến triển)
- A8.2 CLI: ĐANG DỰNG (`agent_cli.py`).
- A4: có `acceptance-gate` + `independent-review` + core-rules §1 — ĐÃ CHẠY THẬT (vd feature Word of the Day qua gate + review độc lập bắt được bug thật).
- A2: ĐÃ có version + changelog + tiêu chí loại bỏ (`memory/KB-CHANGELOG.md`, v3). Có bằng chứng SỬA/XÓA quy tắc sai
  sau khi phát hiện đầu ra lỗi (emoji-tofu, lock per-topic, lint false-positive) + chứng minh đầu ra tốt lên (WotD qua
  gate → review bắt bug). Hướng mốc 4–5. Lệnh: `agent_cli.py kb`.
- A6: ĐÃ khai danh mục 13 việc lặp (`repeat-tasks.md`), **~85% auto hoàn toàn** (11/13; 2 việc cố ý giữ người).
  `agent check` gộp 3 cổng thành 1 lệnh (hướng mốc 5 "loại bỏ việc lặp"). Lệnh: `agent_cli.py check|log|new-skill`.
- A3: VIỆC THẬT = **build app Lingora**. Đã log **6 run Lingora thật** (`product=Lingora iOS`; 4 qua gate, 2 review độc lập)
  — agent dùng trên dữ liệu/việc thật, có log. ⚠️ `baseline_source=agent-estimated` → CHƯA tính tiết kiệm §6;
  cần **CEO đặt baseline (human)** cho từng đầu việc + chạy đều qua thời gian (nhiều phiên) để chứng minh tần suất (mốc 4–5).
