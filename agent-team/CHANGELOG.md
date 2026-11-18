# CHANGELOG — Công ty Agent (SemVer có tầng) (A9)

> **Phân tầng theo độ lớn** (rubric A9 mức 5):
> **MAJOR** (x.0.0) = đổi kiến trúc/luật vận hành · **MINOR** (0.x.0) = thêm năng lực, không phá cái cũ ·
> **PATCH** (0.0.x) = sửa lỗi/tinh chỉnh. Mỗi bản có mục tiêu rõ.
> **Mở lại version cũ:** `git tag` đánh dấu từng mốc → `git checkout v1.0.0` xem lại trạng thái đó.
> File này là người sửa (agent đề xuất qua ADR). Chi tiết vì-sao ở `DECISIONS.md` (ADR).

## [2.2.1] — 2026-11-18  ·  (PATCH) intake --loop sống sót khi mạng chập chờn
- **Sửa** `discord_intake.py`: bắt thêm `URLError/OSError` (vd `ConnectionReset`) + bọc vòng lặp → 1 nhịp
  lỗi mạng KHÔNG giết cả loop (trước đây chết sau ~55 phút vì 1 lần reset). Đúng tinh thần A6 "không vỡ khi gặp bất thường".

## [2.2.0] — 2026-11-17  ·  Siết bảo mật & đánh số version
**Mục tiêu:** nâng A8 (3→4/5) và A9 (4→5) theo tự chấm rubric.
- **Thêm** `docs/access-control.md`: phân loại dữ liệu + phân quyền kênh + runbook thu hồi quyền khi offboard.
- **Thêm** `CHANGELOG.md` (file này) — SemVer phân tầng MAJOR/MINOR/PATCH.
- **Sửa** `discord_intake.py`: `_ack()` nay cũng chạy `redact()` → MỌI đường đẩy ra Discord đều ẩn secret/email.
- Quyết định: ADR-038.

## [2.1.0] — 2026-11  ·  Cổng nhận việc đa người (Discord intake)
**Mục tiêu:** cả team nạp yêu cầu + tài liệu qua 1 kênh chung; agent nạp trọn context để quyết chính xác.
- **Thêm** `discord_intake.py` (đọc kênh qua bot), `channel-log.jsonl` (trọn hội thoại), `triage` 2 tầng → bug/spec/CEO.
- **Thêm** loading-ack tức thì + poll 10s; `docs/discord-intake-setup.md`.

## [2.0.0] — 2026-10/11  ·  Tái cấu trúc "CÔNG TY AGENT"  (MAJOR — đổi kiến trúc)
**Mục tiêu:** chia agent thành công ty 20 skill nhỏ, CEO (người) nắm quyền; đáp rubric đánh giá.
- **Thêm** `.claude/skills/*` (20 skill), CLI `scripts/agent_cli.py`, `ORG.md`, `RUBRIC-MAP.md`.
- **Luật:** ADR-036 ("xong" = acceptance_gate xanh + reviewer độc lập ≠ author), ADR-037 (mô hình công ty skill).
- **Đóng gói lại:** `init_project.py` bê nguyên bộ sang project mới.

## [1.1.0] — 2026-09-27  ·  Loop ngoài kích hoạt thật
**Mục tiêu:** tầng loop ngoài chạy thật (tháng sau khác tháng này).
- **Thêm** cẩm nang `memory/playbooks/test-coverage.md` (ADR-035); gác 20/20 hồi quy, cập nhật baseline.

## [1.0.0] — 2026-09/10  ·  Hệ agent 3 tầng loop chạy thật  (MAJOR — hệ thống đầu tiên hoạt động)
**Mục tiêu:** agent fix-bug chạy end-to-end tới mở PR, 3 tầng loop (trong/giữa/ngoài).
- **Thêm** bộ 20 tình huống hồi quy, pre-commit gate (`scan_secrets`, `ui_lint`), `work_queue`/`outer_loop`/`ingest_bug`.

## [0.1.0] — 2026-09  ·  Bước 0: hạ tầng bộ nhớ + log
- **Thêm** bộ nhớ 5 tầng (`core-rules`/`project-knowledge`/`bugs`/KB) + `run-log` schema + `DECISIONS.md`.

---
### Cách đánh version bản mới
1. Chọn tầng: đổi kiến trúc/luật → **MAJOR**; thêm năng lực → **MINOR**; sửa lỗi → **PATCH**.
2. Ghi 1 mục ở đầu file (mục tiêu + thêm/sửa/bỏ + ADR liên quan).
3. `git tag vX.Y.Z` tại commit chốt bản đó (tag nằm local; đẩy tag là việc người — luật #2).
