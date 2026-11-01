# STATE — đang ở đâu (đọc ĐẦU TIÊN mỗi khi mở context mới)

> Đây là "chỗ đứt" của project. Bất kỳ phiên/agent nào mở lên **đọc file này trước tiên** để tiếp tục,
> KHÔNG làm lại việc đã xong. Là đỉnh của tầng "việc đang làm" (đề bài §4) — giữ NGẮN, luôn cập nhật.
>
> Ai ghi: agent + người, **cập nhật vào CUỐI mỗi phiên làm việc**. Trỏ tới file chi tiết, không chép nội dung.

**Cập nhật lần cuối:** 2026-11-01 — bởi Claude (Opus 4.8)

> ⚠️ ĐÂY LÀ REPO HỆ AGENT (template/framework).

## 🔴 ĐANG CHỜ CEO: merge nhánh `agent-skills-org` → main (luật #2: agent KHÔNG merge)
Nhánh `agent-skills-org` có **8 commit** đã sạch + fast-forward được (main còn cách 8). CEO chạy:
```
!git checkout main && git merge --ff-only agent-skills-org
```
Đây là tái cấu trúc lớn "công ty agent" (xem dưới). Chưa merge thì main vẫn là bản cũ.

## Trạng thái "CÔNG TY AGENT" (tái cấu trúc 2026-10/11 theo rubric đánh giá)
- **Mô hình công ty**: CEO (người) → 6 phòng, mỗi vai trò = 1 Claude Code Skill. Sơ đồ: `agent-team/ORG.md`.
- **20 skill** trong `.claude/skills/*` · **CLI** `scripts/agent_cli.py` (org/skills/skill/workflow/rubric/kb/repeat/replica/check/gate/log/new-skill).
- **Rubric đánh giá** map ở `agent-team/RUBRIC-MAP.md`. Tự chấm: A8✅ A4✅ (Must) · A1~4 A2~4 A3~3 A6~3-4 · A7 (điểm cộng) đã dựng.
- Gate máy: `scripts/{ui_lint,acceptance_gate,health_check}.py` + pre-commit (scan_secrets). KB có version: `memory/KB-CHANGELOG.md`.
- Danh mục việc lặp + auto ~85%: `repeat-tasks.md`. Bản sao CEO: `ceo-profile.md` + skill `my-replica`.
- ADR-036 (xong=gate+reviewer≠author), ADR-037 (công ty skill) trong `DECISIONS.md`.

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
1. **CEO merge** `agent-skills-org` → main (lệnh ở trên) — đang chờ.
2. **A3/A6 lên mốc 4–5**: chạy việc dev THẬT (app Lingora) qua `orchestrate`, đặt baseline (human) **TRƯỚC** mỗi việc, log tích luỹ nhiều phiên. (Hiện đã có 6 run Lingora + baseline hậu-kiểm ~93% tiết kiệm.)
3. **A2 mốc 5**: thêm vài vòng cập nhật KB có version chứng minh đầu ra tốt lên.

## Ghi chú bàn giao cho phiên sau
- **Luật #2 bất khả xâm phạm**: agent KHÔNG merge/phát hành — kể cả khi CEO bảo. CEO tự chạy lệnh merge (đã demo `my-replica` từ chối đúng lệnh này).
- "Xong" giờ = `acceptance_gate.py` xanh + reviewer ĐỘC LẬP ≠ author PASS (ADR-036). Đừng tự ký.
- Emoji trong UI iOS = tofu → `ui_lint.py` chặn; ngoại lệ share-text đánh dấu `// lint:allow-emoji`.
- Lingora iOS từng ở `~/project_personal/Easy-English-IOS` nhưng path đó có lúc KHÔNG còn ở máy — hỏi CEO vị trí trước khi đụng.
