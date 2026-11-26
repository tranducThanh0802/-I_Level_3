# CHANGELOG — khung Agent Team

Quy ước: mỗi phiên bản có **Mục tiêu** và **Thời hạn** (khống chế thời gian). Các phiên bản 0.x–1.0 được ghi lại SAU khi làm, từ lịch sử
git (đánh dấu "ghi nhận sau"): lúc đó chưa đặt thời hạn trước.

## 1.1.0 — 2026-11-20 — Mức 3 rubric: bằng chứng dùng thật + dựng lại được
- **Mục tiêu:** có script chứng minh tần suất dùng và tỷ lệ tự động hoá bằng log; khung có README, VERSION, CHANGELOG.
- **Thời hạn:** 1 ngày (20/11), đặt khi nhận yêu cầu.
- **Kết quả:** `scripts/usage_report.py` (A3, A6), `README.md`, `VERSION`, `CHANGELOG.md`, ADR-036. Chạy thử trên instance ReelMe Android (20 run).
- **Đã làm sau:** git tag v0.1.0, v0.2.0, v1.0.0 (20/11, ghi nhận lại) và v1.1.0.
- **Chưa làm:** thử `init_project.py` trên máy thứ hai.

## 1.0.0 — 2026-09-27 — Chạy thật e2e và đóng vòng cải thiện (ghi nhận sau)
- **Mục tiêu:** chạy thật một app (WeatherApp), retro, kích hoạt loop ngoài. **Thời hạn:** không đặt trước.
- **Kết quả:** Retro #1, #2 (ADR-033, ADR-034), luật #7, `build_review.py`, loop ngoài kích hoạt thật (ADR-035), hồi quy 20/20.

## 0.2.0 — 2026-09-16 — Lấp lỗ hổng của đề bài (ghi nhận sau)
- **Mục tiêu:** lấp 4 lỗ đỏ + các lỗ vàng/xanh. **Thời hạn:** không đặt trước.
- **Kết quả:** baseline + size, vòng review PR, quét secret/PII, idea→spec, hàng đợi, điều phối, dọn bug, bộ 20 tình huống, live feed.

## 0.1.0 — 2026-09-13 — Bước 0: khung + hạ tầng bộ nhớ/log (ghi nhận sau)
- **Mục tiêu:** bộ khung agent-team, bộ nhớ 5 tầng, quản lý per-project, báo cáo §6, bug board. **Thời hạn:** không đặt trước.

## 1.2.0 — kế hoạch (CHỜ NGƯỜI XÁC NHẬN)
- **Mục tiêu đề xuất:** ≥ 1 tuần dùng thật với `baseline_source: human`; git tag mọi phiên bản; thử dựng trên máy thứ hai.
- **Thời hạn đề xuất:** 2026-11-27.
