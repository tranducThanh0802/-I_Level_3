# STATE — đang ở đâu (đọc ĐẦU TIÊN mỗi khi mở context mới)

> Đây là "chỗ đứt" của project. Bất kỳ phiên/agent nào mở lên **đọc file này trước tiên** để tiếp tục,
> KHÔNG làm lại việc đã xong. Là đỉnh của tầng "việc đang làm" (đề bài §4) — giữ NGẮN, luôn cập nhật.
>
> Ai ghi: agent + người, **cập nhật vào CUỐI mỗi phiên làm việc**. Trỏ tới file chi tiết, không chép nội dung.

**Cập nhật lần cuối:** 2026-09-27 — bởi Claude (Opus 4.8)

> ⚠️ ĐÂY LÀ REPO HỆ AGENT (template). **Công việc THẬT đang chạy ở app WeatherApp:**
> `/Users/tranducthanh0802/Project/WeatherApp` — mở `agent-team/STATE.md` của nó để tiếp tục.

## Trạng thái hệ agent (repo này)
- **Đã xây xong, đủ 3 tầng loop chạy THẬT** (trong/giữa/ngoài). 35 ADR trong `DECISIONS.md`.
- Bộ nhớ 5 tầng + playbooks (feature-retro, pr-review-loop, idea-to-spec, orchestrator, ui-ux-review-rubric,
  test-coverage) + scripts (board/report/review/work_queue/outer_loop/ingest_bug/scan_secrets/emit_activity/
  build_*/init_project) + bộ 20 tình huống hồi quy. Đã push GitHub.
- Cẩm nang mới nhất: `test-coverage.md` (sinh từ loop ngoài, ADR-035).

## Đang làm (task còn dở)
- (repo template: không có task code dở — dùng làm khuôn cho project mới qua `init_project.py`)

## Đã xong gần đây (để không làm lại)
- 2026-09-27: Loop ngoài kích hoạt thật lần đầu (ADR-035) — thêm cẩm nang test-coverage, gác hồi quy 20/20.
- Đã sửa bug outer_loop (đếm theo loại). Đã sửa init_project .gitignore + baseline_source/human_minutes.

## Việc kế tiếp (theo thứ tự)
1. _(việc tiếp theo cụ thể)_

## Ghi chú bàn giao cho phiên sau
- _(cạm bẫy, quyết định tạm, chỗ dễ hiểu sai — viết để phiên sau không vấp lại)_
