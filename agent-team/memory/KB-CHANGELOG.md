# Knowledge Base — VERSION & CHANGELOG (A2)

> KB = tập QUY TẮC (core-rules, project-knowledge, playbooks, bugs). File này cho KB cái mà mốc A2 4–5 đòi:
> **phiên bản · nhịp cập nhật xác định · tiêu chí loại bỏ quy tắc cũ · chứng minh đầu ra tốt lên sau mỗi vòng.**

## Phiên bản hiện tại: **v3** (2026-10-29)

## Nhịp cập nhật (ai · khi nào · dựa tín hiệu gì)
- **Ngay lập tức** khi phát hiện ĐẦU RA LỖI do quy tắc sai/thiếu → sửa/thêm quy tắc + ghi changelog (ai: agent đề xuất, **CEO duyệt**).
- **Theo vòng (outer-loop)**: lỗi LẶP ≥3 lần → đề xuất sửa cẩm nang → `run_regression.py` (không tụt baseline) → CEO duyệt → nâng version.
- Tín hiệu kích hoạt: test/review/gate bắt lỗi · người phải sửa tay (ghi `runs.jsonl manual_fixes`) · reviewer độc lập FAIL.

## Tiêu chí LOẠI BỎ quy tắc cũ
- Bị ADR mới đảo ngược (trỏ ngược mục cũ, không xoá lịch sử).
- Mâu thuẫn quy tắc khác (1 luật chỉ ở 1 chỗ — gỡ bản sao).
- Chứng minh có hại/sai bằng đầu ra lỗi.
- Ngoại lệ xuất hiện <3 lần → KHÔNG nhét vào cẩm nang (tránh phình + tự mâu thuẫn, đề §4).

## Changelog (mỗi dòng: tín hiệu → thay đổi → bằng chứng)

### v3 — 2026-10-29
- **THÊM** mô hình công ty + 20 skill + CLI (ADR-037). Tín hiệu: CEO yêu cầu chia nhỏ như tổ chức. Bằng chứng: `ORG.md`, `.claude/skills/*`.
- **THÊM** danh mục việc lặp + auto ~85% (A6). Bằng chứng: `repeat-tasks.md`, `agent check`.

### v2 — 2026-10-11..12 (rút ra từ lỗi đầu ra THẬT)
- **THÊM** luật "'xong' = acceptance gate + reviewer ≠ author, agent không tự ký" (ADR-036). Tín hiệu: CEO "fix UI mãi không biết bao nhiêu lần" — gốc rễ là xong do mắt người/agent tự chấm. Bằng chứng: `acceptance_gate.py`, playbook `acceptance-gate`. **Đầu ra tốt lên:** feature Word of the Day đi qua gate → reviewer độc lập BẮT 1 bug thật (thiếu ProcessingIndicator) mà nếu tự chấm đã lọt.
- **THÊM** luật "không emoji trong UI (tofu) → BrandIcon/SF" + gate `ui_lint`. Tín hiệu: medal 🥇🥈🥉 Leaderboard tofu trên máy. Bằng chứng: `ui_lint.py`.
- **SỬA** quy tắc sai: ban đầu lint cấm MỌI emoji → chặn nhầm chuỗi chia sẻ (render tốt ở iMessage). → thêm ngoại lệ `// lint:allow-emoji`. Tín hiệu: chặn nhầm 1 commit hợp lệ. Bằng chứng: commit sửa lint.
- **SỬA** hiểu sai nguồn chân lý: iOS khoá lesson theo chuỗi tuyến tính toàn level; Android là per-topic. → sửa + PORT test Android làm oracle. Tín hiệu: test cũ TỰ mã hoá hành vi sai (xanh nhưng sai). Bằng chứng: `ProgressionParityTests`.

### v1 — 2026-09 (nền)
- core-rules (không-được-làm, điểm-dừng-hỏi), bộ nhớ 5 tầng, run-log, feature-retro, outer-loop. Bằng chứng: ADR-001..035.

## Chứng minh "đầu ra tốt lên sau mỗi vòng" (mốc 5)
- Trước v2: fix UI lặp nhiều vòng, người tự dò lỗi còn sót.
- Sau v2 (gate + reviewer độc lập): mỗi feature phải enumerate tiêu chí + reviewer ≠ author ký → bug bị bắt TRƯỚC khi tới CEO (vd WotD). Số vòng "sửa đi sửa lại" hội tụ về 1 lượt + 1 review.
