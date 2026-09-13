# PROJECT-CONTEXT — đọc nhanh & định hướng

> Bản đọc-nhanh cho maintainer. Yêu cầu gốc đầy đủ ở `docs/original-spec.md`.
> Lý do đằng sau mỗi quyết định ở `DECISIONS.md`. Luật ràng buộc agent ở `memory/core-rules.md`.

## Mục tiêu

Cắt thời gian con người ở nhóm việc lặp lại của quy trình iOS tại Apero, bằng một agent team
nhận **spec đã bàn giao** làm đầu vào và chạy tới bước **mở PR**. Người vẫn duyệt & merge.

**Đạt (định nghĩa của chủ dự án):** bậc ≥2, thời gian người ở nhóm việc lặp lại giảm ≥40%,
việc bỏ giữa chừng <20%, bug quay lại <10%, số liệu tra được tới từng việc, người khác chạy được.

## Đội hình (cập nhật — xem ADR-010, ADR-009)

**Người:** PO (quyết chức năng, chốt spec, chịu trách nhiệm). Duyệt & merge & phát hành.
**Nguồn đọc:** BE — chỉ đọc, không sửa (đề bài §5).
**Agent:**
- **PO-agent** (trợ lý PO người) — soạn nháp spec *(ADR-010)*; kiêm giám sát: hiểu-spec, cửa hỏi
  (chỉ trả lời từ spec, không có thì leo lên người), canh hướng đi (nêu cờ + bằng chứng). *(ADR-011)*
- **Soát spec** — soi lại spec độc lập + đối chiếu docs BE, chuẩn bị câu hỏi cho PO.
- **UI/UX** — phác thảo/dịch design trong **Penpot tự host** (không limit); người duyệt visual, máy
  kiểm bằng snapshot testing. *(ADR-012)*
- **Dev (Mobile)** — chia task, code, tự soát; kéo design về một mối qua **MCP Penpot** → sinh SwiftUI
  ánh xạ component team.
- **Fix bug** — triage → tra bug cũ → nguyên nhân gốc → sửa + test chống tái phát.
- **Test** — kịch bản đủ 4 trạng thái, chạy thật, quay video.
- **Senior UI/UX** — đánh giá UI: đẹp (đo được→máy, tổng thể→người) / hợp spec / hợp design system.
  Rubric: `memory/playbooks/ui-ux-review-rubric.md`. *(ADR-013)*
- **Reviewer / phản biện** — soi lại để bác bỏ; máy kiểm chốt, không được thì leo lên người. *(ADR-009)*
- *(Bậc 4 mới cần)* Điều phối (orchestrator).

Không thêm: Design/UX agent (phần "nhìn mới biết" để người review qua video), Release/merge agent (cấm nới quyền).

## Bốn agent (mô tả gốc theo đề bài)

| Agent | Vào | Ra | Điểm khó nhất |
|---|---|---|---|
| Soát spec | spec + docs BE | chỗ thiếu/lệch + câu hỏi cho PO | thiếu tiêu chí nghiệm thu / ≥3 trong 4 trạng thái → trả lại spec |
| Dev | spec đã duyệt | PR + mô tả + video + ảnh | tự soát theo chuẩn trước khi báo xong |
| Fix bug | crash store / tester / user / build đỏ | PR + test chống tái phát | **chỉ nguyên nhân gốc, không chữa triệu chứng** |
| Test | tiêu chí nghiệm thu | kịch bản + test chạy thật + video | phủ đủ 4 trạng thái; kết quả thật, không tự thuật |

Bốn trạng thái bắt buộc mọi luồng: **loading, rỗng, lỗi, mất mạng**.

## Hai luồng

- **Feature:** PO → Soát spec → Dev → Test → PR → người merge → build đỏ thì sang fix bug.
- **Bugfix:** nguồn việc → gộp trùng/gán mức/viết lại bước → tra bug cũ → tìm nguyên nhân →
  (BE thì gửi bằng chứng / kiến trúc thì hỏi) → sửa + test → PR → người merge → ghi lại bug cũ.

Sơ đồ đầy đủ ở `docs/original-spec.md` §2.

## Thứ tự xây (quan trọng)

1. **Luồng fix bug trước.** Nguồn việc tự đổ vào từ store/CI, tiêu chí xong rõ, không bị chặn
   bởi chất lượng spec hay lúc PO rảnh.
2. Trong luồng fix bug, bắt đầu từ **crash có stack trace** — nhóm chạy êm nhất (spec §7).
3. Chỉ đụng luồng feature (Soát spec) sau khi fix bug ổn định.
4. Loop ngoài (tự sửa cẩm nang) làm sau cùng.

## Bộ nhớ — 5 tầng

| Tầng | File | Nạp khi | Ai ghi |
|---|---|---|---|
| Luật lõi | `memory/core-rules.md` | luôn | người |
| Việc đang làm | `STATE.md` (đọc đầu tiên) + `workspace/<task>.md` — chỗ đứt, bàn giao, câu hỏi | luôn | **agent** |
| Cẩm nang / playbook | `memory/playbooks/` (chưa tạo) | theo loại việc | người |
| Tri thức dự án | `memory/project-knowledge.md` | theo file đang sửa | người |
| Bug cũ | `memory/bugs/` | khi gặp bug giống | **agent** |

Hai tầng "nạp luôn" phải <2 trang. Agent chỉ ghi được 2 tầng: việc đang làm + bug cũ.

## Loop — 3 tầng

| Loop | Một vòng | Thoát |
|---|---|---|
| Trong | code → build/test | test xanh, hoặc >3 lần |
| Giữa | task → tự soát → PR | đủ tiêu chí nghiệm thu task |
| Ngoài | gom chỗ sửa tay → sửa cẩm nang | chạy định kỳ (chỉ khi lỗi lặp ≥3 lần) |

Vòng hợp lệ = tiêu chí đo được + 1 bước hành động + 1 lần **máy kiểm** + điều kiện thoát.
Chốt chặn chống loop vô hạn: >3 lần / hết ngân sách / 2 vòng giống nhau.

## Đánh giá — số cần theo

Tính từ nhận spec → merge (không tính PO viết spec). Chờ PO **đo riêng**.
Thời gian người/loại việc • tỷ lệ dùng-ngay • số lần sửa tay + 3 loại hay gặp •
việc bỏ giữa chừng • bug gộp trùng • bug quay lại • câu hỏi/tuần.
So sánh: cùng loại, ≥5 mẫu mỗi bên, dùng **median** không dùng mean.

Bốn bậc trưởng thành: 1 (một bước, gọi tay) → 2 (một luồng tự chạy, duyệt 2 đầu) →
3 (cả 2 luồng, tự nhận việc) → 4 (nhiều con + điều phối, tự tìm việc).

## Hiện trạng

- [x] **Bước 0** — hạ tầng bộ nhớ + log (`core-rules.md`, `bugs/`, `logs/run-log.schema.md`).
- [x] Bộ context dự án (file này, `CLAUDE.md`, `DECISIONS.md`, `docs/original-spec.md`, `project-knowledge.md`).
- [x] Nghiên cứu prior art — `docs/prior-art-research.md`.
- [x] Hướng dẫn dựng con Fix bug cho iOS (how-to + kế hoạch tuần 1) — `docs/build-bugfix-agent-guide.md`.
- [x] Dashboard web local — `dashboard.html` + Board + Exchanges + Discord.
- [x] Loop 3 tầng ĐỦ: trong/giữa (build-bugfix-guide) + **ngoài** (`outer_loop.py` + `docs/outer-loop.md`).
- [x] Báo cáo đánh giá §6 — `build_report.py` → report.html (median, chờ ngoài riêng).
- [x] Bộ tình huống hồi quy + cổng chặn — `regression/` + `run_regression.py` (đã test qua/chặn).
- [ ] **CHẶN:** lấp `project-knowledge.md` (cần đường dẫn repo iOS thật: lệnh build/test, nguồn crash, BE).
- [ ] Bước 1 — con Fix bug làm một bước, gọi tay (bậc 1) — theo kế hoạch tuần 1 trong guide.
- [ ] Phép thử bộ nhớ — báo lại bug mẫu, kiểm agent có tra ra cách sửa cũ.
- [ ] Bước 2 — đóng chốt chặn loop trong.
- [ ] Bước 3 — Fix bug chạy liền cả luồng (bậc 2).

_Cập nhật mục này mỗi khi có tiến triển._
