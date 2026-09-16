# DECISIONS — nhật ký quyết định (ADR rút gọn)

> Mỗi quyết định một mục: bối cảnh → chọn gì → vì sao → hệ quả. Đọc file này TRƯỚC khi
> đổi bất cứ gì trong `agent-team/`, để không phá một quyết định đã có lý do.
> Không xoá mục cũ; nếu đảo quyết định thì thêm mục mới trỏ ngược lại mục cũ.

---

## ADR-001 — Bắt đầu từ luồng fix bug, không phải luồng feature
- **Ngày:** 2026-09-13
- **Bối cảnh:** Có 2 luồng (feature, bugfix). Hỏi nên bắt đầu từ đâu.
- **Quyết định:** Xây luồng **fix bug** trước; trong đó bắt đầu từ **crash có stack trace**.
- **Vì sao:** Nguồn việc tự đổ vào từ store/CI; tiêu chí "xong" đo được bằng máy (test cũ+mới xanh);
  không bị chặn bởi chất lượng spec hay lúc PO rảnh (spec §2). Crash có stack trace là nhóm
  chạy êm nhất (spec §7). Feature bị chặn bởi chất lượng spec → rủi ro cao hơn.
- **Hệ quả:** Con Soát spec và luồng feature làm sau. Phép thử đầu tiên KHÔNG dùng nhóm việc khó
  (kiến trúc giữa đường, race condition, spec mơ hồ).

## ADR-002 — Bộ nhớ nằm trong repo, phân 5 tầng, agent chỉ ghi 2 tầng
- **Ngày:** 2026-09-13
- **Quyết định:** Mọi bộ nhớ là file trong repo (không nằm trong tài khoản riêng ai). Agent CHỈ được
  ghi vào "việc đang làm" và "bug cũ". Cẩm nang + tri thức dự án + luật lõi do **người** sửa.
- **Vì sao:** Người khác phải mở đọc được (spec §3, §5 "người khác bấm thử phải chạy được").
  Cho agent tự sửa cẩm nang của chính nó → hai tuần sau không ai biết luật nào còn hiệu lực.
- **Hệ quả:** Loop ngoài (sửa cẩm nang) luôn qua người duyệt. Một luật chỉ nằm ở một chỗ.

## ADR-003 — "Xong" phải máy kiểm được; agent tự khen không tính
- **Ngày:** 2026-09-13
- **Quyết định:** Mọi tiêu chí "xong" = thứ chạy được trả về đúng/sai (build/test/lint/so ảnh/
  agent khác đọc theo checklist). Bàn giao bắt buộc có video + ảnh trước/sau.
- **Vì sao:** Chỗ hầu hết mọi người làm hỏng loop là tin lời agent tự báo (spec §4). Nhìn diff
  không đoán được UI đúng/sai, mà tự build chạy thử thì mất đúng thời gian đang cắt (spec §5).
- **Hệ quả:** Chưa có video/ảnh = chưa xong. Không nhận tiêu chí kiểu "làm cho đẹp".

## ADR-004 — Không nới quyền merge/đẩy store cho agent
- **Ngày:** 2026-09-13
- **Quyết định:** Agent dừng ở mở PR. Người duyệt, merge, phát hành. Vĩnh viễn, kể cả sau nhiều tháng êm.
- **Vì sao:** Spec §5 nêu rõ. Rủi ro của merge/phát hành sai không đối xứng với lợi ích tốc độ.

## ADR-005 — CSDL bug có fingerprint + đếm + nhãn được/không được
- **Ngày:** 2026-09-13
- **Quyết định:** Mỗi bug có `fingerprint` (nhận trùng), `count` (đếm lần lặp), và `outcome`
  được/không được trên TỪNG lần thử (kể cả thất bại). Dọn định kỳ bug gắn code đã xoá.
- **Vì sao:** Bộ đếm cho biết lỗi lặp ≥3 lần → đầu vào loop ngoài. Thiếu nhãn thất bại thì lần sau
  tra ra rồi lặp lại đúng cái sai, nhìn ngoài tưởng đang học (spec §3).
- **Hệ quả:** Con Fix bug bắt buộc tra `fingerprint` trước khi sửa, ghi lại `outcome` sau khi sửa.

## ADR-006 — Bước 0 làm trước khi viết agent nào
- **Ngày:** 2026-09-13
- **Quyết định:** Dựng hạ tầng (core-rules, bug DB schema + ví dụ, run-log schema) trước khi
  thiết kế bất kỳ agent nào.
- **Vì sao:** Agent Fix bug cần đọc core-rules và ghi bug DB ngay từ lần chạy đầu; không có log
  thì mục 6 (đánh giá) không đo được gì. Không có nền thì agent không có chỗ đứng.

## ADR-007 — Đo, đánh giá bằng median và tách thời gian chờ ngoài
- **Ngày:** 2026-09-13
- **Quyết định:** So sánh cùng loại việc, ≥5 mẫu/bên, dùng **median**. `wait_external_ms` (chờ PO/BE)
  đo nhưng để riêng, không gộp vào thời gian làm.
- **Vì sao:** Một việc dài bất thường kéo lệch mean về hướng có lợi cho người báo cáo (spec §6).
  Chờ PO agent không cắt được → gộp vào là ra số xấu vì lý do không phải lỗi hệ thống.

## ADR-008 — Hàng rào chống-đi-sai-hướng tạm để ở mức quy ước (chưa cưỡng chế bằng máy)
- **Ngày:** 2026-09-13
- **Bối cảnh:** Đã có luật văn bản (CLAUDE.md, core-rules, DECISIONS, spec bất biến) nhưng chưa có
  hook máy nào ép buộc. Hỏi có dựng cưỡng chế (PreToolUse chặn sửa test/spec) không.
- **Quyết định:** **Chưa dựng hook cưỡng chế** — giữ ở mức quy ước. Dựng hook sau.
- **Vì sao:** Chủ dự án chọn ưu tiên tiến độ, chưa cần khoá cứng ở giai đoạn nền.
- **Hệ quả / rủi ro đã biết:** Chưa có gì *chặn* agent sửa file test cho "test xanh" (reward-hacking) —
  research xác định đây là cạm bẫy dễ âm thầm phá nhất. Khi dựng con Fix bug thật, cân nhắc bật lại:
  hook `PreToolUse` chặn ghi test/CI + tách `test-author` (chỉ tạo file test mới) khỏi `bugfix-agent`
  (khoá toàn bộ test). Chi tiết: `docs/build-bugfix-agent-guide.md` §1.3.

## ADR-009 — Có "nơi phản biện có cấu trúc"; máy kiểm chốt, không kiểm được thì leo lên người
- **Ngày:** 2026-09-13
- **Bối cảnh:** Ý chủ dự án: cần một nơi để các con "trao đổi/tranh cãi" thì mới ra kết quả tốt nhất.
- **Quyết định:** Có nơi chung dạng **blackboard file trong repo** (`agent-team/reviews/review-<task>.md`),
  người + agent cùng đọc/ghi. Nhưng theo **hình thức phản biện có cấu trúc**, KHÔNG phải chat cãi tự do:
  con *làm* nêu giả thuyết + bằng chứng → con *phản biện* (context mới, nhiệm vụ là **bác bỏ**) → 
  **kết luận do MÁY KIỂM chốt** (build/test/lint/so ảnh); chỗ máy không kiểm được (nguyên nhân gốc
  hợp lý không, UI/cảm giác) thì đóng gói **2 phương án + hệ quả** gửi **người** quyết.
- **Chốt chặn:** tối đa 2–3 vòng phản biện; hết thì dừng, leo lên người. Không cãi vô hạn (đề bài §4).
- **Vì sao:** Research (MAST NeurIPS 2025: ~79% lỗi multi-agent do phối hợp/đặc tả; Cognition "Don't
  Build Multi-Agents") cảnh báo cãi tự do sinh giả định mâu thuẫn & tốn token. **Đồng thuận ≠ đúng** —
  lấy "hai con đồng ý" làm điều kiện dừng là tin vào lời khen lẫn nhau, đúng cái đề bài §4 cấm.
- **Hệ quả:** Con Test + một con reviewer đóng vai phản biện. Blackboard = working-state (agent ĐƯỢC
  ghi). Với luồng feature, người xử phản biện là **PO**, không phải một con đoán thay. Mẫu:
  `agent-team/reviews/review-EXAMPLE.md`.

## ADR-010 — Thêm agent trợ lý soạn spec; PO người vẫn sở hữu & chốt. BE giữ chỉ-đọc
- **Ngày:** 2026-09-13
- **Bối cảnh:** Chủ dự án muốn có con lo phần tài liệu/chức năng. Đề bài gốc để PO hoàn toàn là người.
- **Quyết định:**
  - **PO vẫn là người** — quyết định chức năng, sửa lại và **chốt** spec, chịu trách nhiệm hướng đi.
  - Thêm **agent "spec-drafter" (trợ lý PO)**: soạn NHÁP spec cho *chi tiết & đầy đủ* (đủ 4 trạng thái
    loading/rỗng/lỗi/mất mạng, tiêu chí nghiệm thu máy-kiểm-được, cái gì lần này không làm, API dùng).
    Lý do: người khó tự viết đủ chi tiết — đây đúng là gốc của "spec mơ hồ", nhóm nguy hiểm nhất.
  - **BE giữ chỉ-đọc** theo đề bài §5. Không dựng BE-agent sửa. Bug do BE → đóng gói bằng chứng gửi sang.
- **Ranh giới quan trọng (chống lẫn với con Soát spec):**
  - `spec-drafter` **tạo** nháp. `Soát spec` **soi lại độc lập** (context mới, nhiệm vụ bác bỏ) —
    người tạo không được tự chấm mình (nguyên tắc ADR-009). Người PO chốt ở giữa/cuối.
  - Luồng: PO nêu ý → spec-drafter soạn nháp → PO sửa → Soát spec soi + đối chiếu docs BE → PO chốt →
    spec chốt là đầu vào cho Dev.
- **Hệ quả:** Đề bài (bản gốc) KHÔNG sửa; điều chỉnh này sống ở ADR này. Cách đánh giá "cắt thời gian
  người" vẫn đúng: giờ đo cả thời gian người viết spec nhờ có trợ lý.

## ADR-011 — PO-agent kiêm giám sát: hiểu-spec, định tuyến câu hỏi, canh hướng đi
- **Ngày:** 2026-09-13
- **Bối cảnh:** Chủ dự án muốn con PO-agent (từ ADR-010) còn giám sát spec, hỏi lại chỗ chưa hiểu,
  và theo dõi các con khác có đi đúng hướng không.
- **Quyết định:** Mở rộng PO-agent thành vai **điều phối / giám sát** (trợ lý của PO người), làm 3 việc:
  1. **Giám sát hiểu-spec** — mọi con bám đúng spec chốt; phát hiện mơ hồ. Chốt bằng **máy** (tiêu chí
     nghiệm thu + đủ 4 trạng thái).
  2. **Cửa hỏi** — nhận câu hỏi từ các con; **chỉ trả lời nếu có sẵn nguyên văn trong spec (kèm trích dẫn)**,
     không có thì leo lên **PO người** theo mẫu 30 giây (đề bài §5). **Cấm bịa câu trả lời.**
  3. **Giám sát hướng đi** — theo dõi bám spec + luật lõi; nghi lệch thì **nêu cờ kèm bằng chứng**.
     Việc đo được → **máy** chốt; việc chủ quan → **PO người** chốt.
- **Ba rào cứng (chống rubber-stamp / ảo giác "mọi thứ ổn"):**
  - PO-agent KHÔNG tự sửa spec, KHÔNG tự nới quyền/merge.
  - Mọi phán "đúng hướng/lệch" phải kèm bằng chứng (trích spec + tín hiệu máy) — cấm gật suông.
  - Mọi flag/escalation ghi vào log + blackboard (`reviews/`), tra lại được.
- **Vì sao:** Con giám sát tự phán "đội đang đúng hướng" là tự khen (đề bài §4, ADR-009 cấm); MAST gọi
  là reasoning-action mismatch — giám sát ảo giác ổn trong khi đã lệch. Nên nó PHÁT HIỆN & nêu cờ,
  không phải người phán cuối ở chuyện chủ quan.
- **Ranh giới với con khác (một luật một chỗ):** Soát spec = cổng vào (chất lượng spec, một lần);
  Reviewer = cổng ra (một sản phẩm/task); PO-agent = giám sát quá trình xuyên suốt. Không đè nhau.

## ADR-012 — Thêm con UI/UX, nối Penpot tự host; Mobile kéo về một mối qua MCP; người duyệt visual
- **Ngày:** 2026-09-13
- **Bối cảnh:** Chủ dự án muốn con UI/UX vẽ được và Mobile kéo về một mối, **không bị limit**.
  (Đảo lại quyết định cũ "không dựng Design agent".)
- **Quyết định:**
  - Thêm **con UI/UX** — **phác thảo / dịch design ra code**, KHÔNG phải tự vẽ UI hoàn chỉnh.
  - Nối **Penpot tự host** (open-source, không giới hạn ghế/lượt gọi, miễn phí; có MCP server từ 12/2025).
  - **"Một mối":** Penpot mở cổng MCP/API → con **Mobile đọc từ đúng cổng đó** làm nguồn duy nhất →
    sinh **SwiftUI ánh xạ vào component có sẵn của team** (map component, không sinh code linh tinh).
- **Vì sao Penpot:** "Không bị limit" là ưu tiên số 1. Figma miễn phí chỉ 6 lần gọi MCP/tháng; bỏ cap
  phải trả tiền theo ghế Dev/Full. Penpot tự host bỏ mọi giới hạn đó. Đánh đổi đã chấp nhận: tự bảo trì,
  hệ sinh thái nhỏ hơn Figma.
- **Rào cứng (vì UI/UX là nhóm "phải nhìn mới biết" — agent yếu nhất):**
  - **Người bắt buộc duyệt visual** (qua video + ảnh trước/sau — đề bài §5). Agent KHÔNG tự chốt đẹp/xấu.
  - **Máy kiểm = snapshot testing** (swift-snapshot-testing): so ảnh với baseline người đã duyệt; hook
    chặn agent tự tạo/ghi baseline để ép pass (như guide §2.3). Để advisory tới khi baseline ổn định.
  - UI/UX sinh **từ design system/component ràng buộc**, không sáng tạo tự do → giảm rủi ro & dễ review.
- **Hệ quả:** Cần dựng hạ tầng Penpot tự host + kết nối MCP (việc BE/DevOps của team, ghi vào
  project-knowledge.md khi làm). Đây là việc SAU khi con Fix bug chạy ổn; không phải ưu tiên trước mắt.
- **Stack cụ thể (research `docs/ai-uiux-tooling-research.md`):** KHÔNG có công cụ Penpot→SwiftUI trực
  tiếp. Cầu nối = **penpot-export (tokens JSON) + LLM sinh SwiftUI theo skill DESIGN.md mô tả component
  team + swift-snapshot-testing làm cổng người duyệt**. MCP: `penpot/penpot` (/mcp) chính thức, dự phòng
  `zcube/penpot-mcp-server`. Asset SVG: `swhitty/SwiftDraw`. Lưu ý: claim "Penpot xuất token SwiftUI" là
  SAI (docs chính thức chỉ JSON/DTCG).

## ADR-013 — Thêm con Senior UI/UX (đánh giá UI): đẹp / hợp spec / hợp UI đang làm
- **Ngày:** 2026-09-13
- **Bối cảnh:** Chủ dự án muốn con senior UI/UX đánh giá UI vừa sinh: có đẹp không, hợp spec không,
  hợp UI đang làm không.
- **Quyết định:** Thêm con **Senior UI/UX** — reviewer chuyên UI (read-only critique, không sửa code).
  Đánh giá 3 trục, mỗi trục chốt khác nhau:
  1. **Đẹp** — chấm phần đo được (tương phản WCAG, thang spacing, touch target ≥44pt, hệ typography):
     **máy chốt**. Phần tổng thể/cảm giác: agent NÊU cụ thể có dẫn chứng, **người duyệt cuối** — cấm tự chốt "đẹp".
  2. **Hợp spec** — checklist đủ 4 trạng thái, đủ thành phần, đúng luồng/label: **máy/checklist chốt**.
  3. **Hợp UI đang làm** — lint: dùng component team, màu/chữ/spacing từ tokens (không hardcode), so
     snapshot màn cùng loại: **máy chốt**.
- **Verdict:** trục 2 hoặc 3 FAIL → trả lại (máy). Đạt máy → chuyển người duyệt phần "đẹp".
- **Vì sao:** "Đẹp" là nhóm "phải nhìn mới biết" — agent yếu nhất, người phải chốt (đề bài §7, ADR-009).
  Nhưng phần lớn "hợp spec / hợp design system" LÀ đo được → giao máy, giảm việc cho người.
- **Ranh giới (một luật một chỗ):** Test = 4 trạng thái *chạy được* (chức năng); Senior UI/UX = *chất
  lượng thị giác + nhất quán design system + hợp spec của UI*; Reviewer = đúng/sai logic sản phẩm.
- **Rào chống dấu cao su:** mỗi PASS/FAIL kèm bằng chứng (rule/dòng spec/tên token/ảnh), ghi vào `reviews/`.
- **Công cụ:** rubric `memory/playbooks/ui-ux-review-rubric.md`; máy kiểm visual = swift-snapshot-testing.

## ADR-014 — Dựng workspace/: nơi bàn giao giữa các con + định tuyến câu hỏi (tầng "việc đang làm")
- **Ngày:** 2026-09-13
- **Bối cảnh:** "Nơi trao đổi" mới có reviews/ (phản biện) + bugs/ (tri thức) + logs/. Thiếu chỗ cụ thể
  cho tầng "việc đang làm": bàn giao giữa các con, đang ở bước nào, câu hỏi lên người.
- **Quyết định:** Mỗi task một file `workspace/<task>.md` — kế hoạch + bước hiện tại + log bàn giao
  (con nào giao con nào) + câu hỏi lên người (mẫu 30 giây) + trạng thái chờ. Agent ĐƯỢC ghi. Trỏ tới
  review & bug liên quan.
- **Vì sao:** Đề bài §3 có tầng "việc đang làm", §4 buộc trạng thái nằm ngoài context (tắt/mở lại tiếp
  được), ADR-011 cần "cửa hỏi" cụ thể. Trước đó mới có nguyên tắc, chưa có chỗ.
- **Bản đồ nơi trao đổi (một luật một chỗ):** workspace = việc đang làm/bàn giao/câu hỏi · reviews =
  phản biện + verdict · bugs = tri thức bug · logs = nhật ký chạy · memory = luật & cẩm nang (người sửa).

## ADR-015 — Discord là bản chiếu real-time; git là gốc. Bug & spec cũng đẩy ra Discord
- **Ngày:** 2026-09-13
- **Quyết định:** Đẩy trao đổi (workspace/reviews), bug (memory/bugs), spec (specs) ra Discord real-time
  qua 2 webhook: phòng "agent trao đổi" + phòng "agent ↔ user" (câu hỏi chặn, tô đỏ). Mỗi agent 1 màu.
- **Nguyên tắc:** **Git = chân lý; Discord = màn hình + báo động.** Không quyết định trong chat rồi trôi mất
  (giữ đề bài §3: mọi thứ trong repo, đọc được). Webhook URL để trong `scripts/discord_config.json`,
  đã `.gitignore` (là bí mật). Không đẩy secret/dữ liệu user ra Discord.
- **Công cụ:** `scripts/post_to_discord.py` (đăng tin mới, dedup theo state). 1 webhook/phòng, mỗi agent
  tự xưng tên+màu qua embed (không cần mỗi agent 1 webhook).

## ADR-016 — Kiểm soát spec: thư mục specs/ có gating; bug kiểm soát ở memory/bugs/ (đã có)
- **Ngày:** 2026-09-13
- **Bối cảnh:** Hỏi có nơi kiểm soát bug & spec không. Bug: đã có `memory/bugs/` (ADR-005). Spec từng
  feature: CHƯA có chỗ quản lý trạng thái duyệt.
- **Quyết định:** Thêm `agent-team/specs/<feature>.md` với **gating trạng thái**:
  `draft → reviewing → approved → building → done`. **Dev CHỈ bắt đầu khi `status: approved`**;
  chỉ **PO người** đổi được sang `approved`. Đổi spec sau approved → tăng `version` (+ changelog).
- **Ai ghi:** spec-drafter soạn nháp; Soát spec soi (trả lại nếu thiếu tiêu chí nghiệm thu / ≥3 trạng thái);
  PO người duyệt. Bug: Test ghi (source=tester), Fix bug triage/ghi kết quả.
- **Vì sao:** "Kiểm soát" = có cổng duyệt đo được, không để Dev tự đoán từ spec chưa chốt (đề bài §1, §5).

## ADR-017 — Đây là bộ khung mẫu; mỗi project là một bản sao riêng có web quản lý riêng
- **Ngày:** 2026-09-13
- **Bối cảnh:** Chủ dự án xác định: form hiện tại là mẫu; mỗi project thật sẽ có 1 web quản lý riêng.
- **Quyết định:** Repo này = **template/kit**. Mỗi project = bản sao độc lập: dữ liệu riêng
  (specs/workspace/reviews/bugs/logs), 3 web riêng (dashboard/board/exchanges), webhook Discord riêng.
  Tạo bằng `scripts/init_project.py <đích> "Tên"`. Các trang đọc `project.config.json` để hiện tên project.
- **Dùng chung vs riêng:** chung = core-rules, playbooks, scripts, cấu trúc, docs. Riêng = config,
  specs/workspace/reviews/bugs/logs, project-knowledge, discord_config (webhook).
- **Vì sao:** Dữ liệu/PR/bug/webhook của các project phải tách biệt; một bộ khung tái dùng giúp mỗi
  project lên nhanh mà vẫn cùng chuẩn. Bí mật (webhook/state) không copy, không vào repo.
- **Hướng dẫn:** `docs/new-project-setup.md`.

## ADR-018 — Cô lập giữa project + liên tục trong project (STATE.md + giao thức resume)
- **Ngày:** 2026-09-13
- **Bối cảnh:** Cần: (a) project mới không dính context project cũ; (b) cùng project, kill/mở lại các
  context hiểu nhau, không làm sai/làm lại.
- **Quyết định:**
  - **Cô lập:** "trí nhớ" là FILE trong thư mục từng project. `init_project.py` tạo project rỗng
    (specs/workspace/reviews/bugs/logs rỗng, STATE.md reset). Context chỉ đọc thư mục project hiện tại,
    không dựa trí nhớ chat. (Bộ nhớ bền của Claude cũng khoá theo đường dẫn project → tự cô lập.)
  - **Liên tục:** thêm `agent-team/STATE.md` = điểm vào "đọc đầu tiên" (việc dở/đã xong/kế tiếp). CLAUDE.md
    có **giao thức resume**: mở context mới → đọc STATE → core-rules → workspace → bugs/DECISIONS khi cần.
    Cuối phiên phải cập nhật STATE + workspace ("chỗ đứt").
- **Vì sao:** Đề bài §4 buộc trạng thái nằm ngoài context để tắt/mở lại tiếp được; bugs/ có fingerprint+outcome
  nên không sửa lại bug cũ; logs ghi việc đã chạy → không làm lại.
- **Hệ quả:** Bỏ cập nhật STATE cuối phiên = phiên sau làm lại. Giữ STATE ngắn (<2 trang).

## ADR-019 — BE là tuỳ chọn (tuỳ loại app); khung không mặc định luôn có backend
- **Ngày:** 2026-09-13
- **Bối cảnh:** Chủ dự án nêu: BE có thể không có, tuỳ loại app (offline/local-only).
- **Quyết định:** Khai báo "có BE không" ở `project-knowledge.md`. Ranh giới BE (core-rules §3) **chỉ áp
  khi có BE**. App không BE → bỏ qua phần đó; nhưng luật "không tự đổi cấu trúc dữ liệu lưu local"
  (§1) vẫn áp; và spec field `api:` ghi "local-only".
- **Vì sao:** Không phải app nào cũng có backend; mặc định luôn-có-BE sẽ đẻ ra luật/câu hỏi vô nghĩa
  cho app offline.
- **Hệ quả:** Fix bug flow "bug do BE → gửi bằng chứng" chỉ dùng khi có BE. Con Soát spec kiểm "API dùng"
  → với app không BE thì xác nhận nguồn dữ liệu local thay vì API.

## ADR-020 — Báo cáo đánh giá (§6): tính số từ log, dùng median
- **Ngày:** 2026-09-13
- **Quyết định:** `scripts/build_report.py` → `report.html`: thời gian theo loại việc (**median**), chờ
  ngoài để RIÊNG, tỷ lệ dùng-ngay, top-3 loại sửa tay, % bỏ dở, bug gộp trùng, **bug quay lại**, câu hỏi.
- **Vì sao:** §6 "không có số thì chưa đạt". Cờ cảnh báo: bỏ-dở 0% = có thể giấu; <5 mẫu = chưa kết luận.

## ADR-021 — Bộ tình huống hồi quy + cổng chặn (§4 tầng ngoài)
- **Ngày:** 2026-09-13
- **Quyết định:** `agent-team/regression/` (scenarios.jsonl + baseline.json + results) và
  `scripts/run_regression.py`: chạy sau khi đổi cẩm nang/chuẩn; tỷ lệ đạt **tụt dưới baseline → CHẶN (exit 1)**.
- **Vì sao:** §4 "giữ bộ tình huống, chạy lại khi cẩm nang/chuẩn đổi, tệ đi thì chặn; sửa hỏng 1 dòng
  cẩm nang bộ này phải bắt được". Đã test: 100%→qua, 90%→chặn.
- **Hệ quả:** Hiện có 10 tình huống hạt giống; **cần góp đủ 20 từ việc thật** khi hệ chạy. Baseline do người duyệt.

## ADR-022 — Loop ngoài: gom sửa tay → lỗi lặp ≥3 → đề xuất cẩm nang → người duyệt → hồi quy
- **Ngày:** 2026-09-13
- **Quyết định:** `scripts/outer_loop.py` gom `manual_fixes` từ logs, **chỉ đề xuất** khi một lỗi lặp
  ≥3 lần (ghi `outer-loop-proposals.md`); người duyệt & sửa cẩm nang; rồi `run_regression.py` chốt cổng;
  cập nhật baseline. Quy trình đầy đủ: `docs/outer-loop.md`.
- **Vì sao:** §4 "tầng ngoài mới khiến tháng sau khác tháng này". Ba rào: ngưỡng ≥3 (tránh cẩm nang phình),
  bộ hồi quy (tránh làm tệ đi), người duyệt (agent không tự sửa cẩm nang — ADR-002).
- **Hệ quả:** Đủ 3 tầng loop (trong/giữa/ngoài) như đề bài yêu cầu.

## ADR-023 — Bug board kiểu Jira tối giản; bug agent bó tay → cột "Cần người" + báo Discord
- **Ngày:** 2026-09-13
- **Bối cảnh:** Cần trình quản lý bug giống Jira nhưng đơn giản, mục tiêu: bug agent không fix được thì
  người nhảy vào làm được.
- **Quyết định:** `scripts/build_bugboard.py` → `bugboard.html` — kanban 5 cột: Mới · Đang xử lý ·
  **🙋 Cần người** · Đã sửa · Bỏ qua. Cột "Cần người" gộp `needs-arch/be-side/cant-repro/needs-human`
  (đúng 3 điểm dừng của Fix bug trong đề bài §1). Thêm field bug: `assignee`, `stuck_reason`.
  Người nhận bug: sửa file → `assignee=tên`, `status=in-progress`. Bug "cần người" cũng đẩy ra Discord
  phòng hỏi-người (🙋 BUG CẦN NGƯỜI).
- **Vì sao:** Biến "agent DỪNG" thành "người tiếp quản" trơn tru; nguồn dữ liệu vẫn là `memory/bugs/`
  (git = gốc), board chỉ là màn hình. Không dựng Jira thật để tránh phụ thuộc ngoài + giữ mọi thứ trong repo.
- **Hệ quả:** Chỉnh trạng thái/nhận việc = sửa file .md (board tĩnh không ghi được). Đủ đơn giản, ai cũng làm được.

## ADR-024 — PO-agent: pipeline ý tưởng → research → spec draft (người chốt)
- **Ngày:** 2026-09-14
- **Bối cảnh:** Cần đưa một ý tưởng thô để PO-agent research và biến thành spec/tài liệu.
- **Quyết định:** Mở rộng PO-agent: ý tưởng (1–2 câu) → (1) làm rõ/hỏi → (2) research có nguồn →
  (3) sinh `specs/<feature>.md` status **draft** (đủ tiêu chí nghiệm thu + 4 trạng thái + mục Căn cứ/Research
  + câu hỏi mở) → (4) Soát spec soi → **PO người chốt approved**. Cẩm nang: `memory/playbooks/idea-to-spec.md`.
- **Rào:** agent ĐỀ XUẤT không QUYẾT (không tự đặt approved, không tự quyết phạm vi sản phẩm); mọi claim
  research có NGUỒN, không bịa (tránh spec mơ hồ — nhóm nguy hiểm nhất). Dùng WebSearch/skill deep-research.
- **Hệ quả:** Lấp lỗ hổng "ý tưởng → tài liệu". Không phá đề bài vì PO người vẫn giữ quyết định & chốt spec.

## ADR-025 — Log thêm `size` + `human_baseline_min` để tính "tiết kiệm ≥40%" (§6)
- **Ngày:** 2026-09-14
- **Bối cảnh:** Lỗ hổng #1+#2: không có baseline người-làm-tay → không tính được "giảm ≥40%"; và không
  có độ khó → so sánh không công bằng (§6 "độ khó tương đương").
- **Quyết định:** `runs.jsonl` thêm `size` (S/M/L, bắt buộc) và `human_baseline_min` (ước lượng làm tay).
  Báo cáo web + Excel tính **Tiết kiệm = (baseline − thời-gian-agent)/baseline**, median, theo loại; KPI
  xanh khi ≥40%. Việc thiếu baseline không vào phép tính.
- **Vì sao:** Không có 2 trường này thì dù chạy e2e xong vẫn không trả lời được câu hỏi chính của §6.

## ADR-026 — Vòng phản hồi review PR (người chê → agent sửa → người merge)
- **Ngày:** 2026-09-14
- **Bối cảnh:** Lỗ hổng #3: agent mở PR nháp rồi DỪNG; chưa có vòng người-trong-lặp.
- **Quyết định:** `pr_status` (draft→changes-requested→approved→merged) + `review_round` ở workspace;
  người ghi feedback checklist ("## Phản hồi review PR"), agent sửa từng ý + máy kiểm xanh + đánh dấu.
  Chốt chặn ≤3 vòng, 2 vòng giống nhau thì dừng. Agent KHÔNG merge. Cẩm nang: `playbooks/pr-review-loop.md`.

## ADR-027 — Cổng quét SECRET + PII trước commit / gửi Discord
- **Ngày:** 2026-09-14
- **Bối cảnh:** Lỗ hổng #4: agent sửa code thật có thể lộ khóa; crash log có thể chứa PII → rò ra Discord.
- **Quyết định:** `scripts/scan_secrets.py` — SECRET (private key/AWS/Google/webhook/JWT/khóa-gán-biến/file .p12…)
  → CHẶN (exit 1); PII (email/SĐT) → cảnh báo. Cài pre-commit hook: `--install-hook`. Discord poster tự
  **redact** email/secret trước khi gửi. Đã test: repo sạch qua, secret giả bị chặn.

## ADR-028 — Hàng đợi ưu tiên (agent lấy việc gì tiếp)
- **Ngày:** 2026-09-16 · Lỗ hổng #5.
- **Quyết định:** `scripts/work_queue.py` xếp hạng: bug điểm = mức_nặng*10 + số_lần_lặp (bug 'cần người'
  tách riêng); spec theo `priority` P0>P3 (approved→Dev, reviewing→Soát spec). Ghi `work-queue.md`.
  Thêm field `priority` vào specs.

## ADR-029 — Adapter nạp bug tự động từ store/CI (gộp trùng)
- **Ngày:** 2026-09-16 · Lỗ hổng #7 (Bậc 3 "tự nhận việc").
- **Quyết định:** `scripts/ingest_bug.py` nhận crash (exc/frame/method/source) → tính fingerprint chuẩn
  hoá (bỏ số dòng/offset/closure) → **trùng thì count++**, mới thì tạo BUG-<n>. Crashlytics/Sentry/CI gọi
  script này. Đã test: mới→tạo, lặp→count=2.

## ADR-030 — Con điều phối / Quản đốc (Bậc 4, thiết kế sẵn)
- **Ngày:** 2026-09-16 · Lỗ hổng #6.
- **Quyết định:** Playbook `playbooks/orchestrator.md`: đọc hàng đợi → giao đúng agent → theo dõi → leo
  thang (bug cần người / >3 vòng review / chạm nhóm cấm) → cân tải (không 2 agent đụng 1 file). Trần
  2–3 agent song song. **Kích hoạt khi lên Bậc 4**; trước đó điều phối tay bằng work_queue. Điều phối
  KHÔNG nới quyền (không merge/không sửa cẩm nang).

## ADR-031 — Dọn bug định kỳ + chi phí + bộ 20 tình huống + spec đổi giữa chừng (🟢)
- **Ngày:** 2026-09-16 · Lỗ hổng #8, #10, #11, #9.
- **Quyết định:**
  - `scripts/cleanup_bugs.py`: archive bug fixed/wontfix quá 90 ngày + cảnh báo bug gắn file đã xoá (§3 "dọn định kỳ").
  - Log thêm `cost_usd` (tùy chọn) → báo cáo tổng chi phí token.
  - Bộ hồi quy nâng **10 → 20 tình huống** (đủ theo đề bài §4); run_regression 20/20.
  - Spec đổi giữa chừng: specs đã có luật tăng version + changelog (đổi lớn → quay lại reviewing) + tình huống R16.

## ADR-032 — Theo dõi agent chạy trực tiếp (live activity feed)
- **Ngày:** 2026-09-16
- **Bối cảnh:** Trước khi cho agent chạy thật, cần xem được nó đang làm gì realtime (không chỉ ảnh chụp).
- **Quyết định:** 3 tầng theo dõi: **Live** (`emit_activity.py` phát sự kiện từng bước → `live/activity.jsonl`;
  xem bằng `watch_live.py` trong terminal hoặc Discord nếu `--discord`), **Ảnh chụp** (dashboard/board/report),
  **Hồi cứu** (runs.jsonl + report). `activity.jsonl` ephemeral (.gitignore); hồ sơ chính thức vẫn là runs.jsonl.
- **Vì sao:** Quan sát lúc chạy là điều kiện để tin tưởng + can thiệp sớm khi agent đi sai. Đã test: feed
  màu trong terminal + đẩy Discord realtime.

## Ghi chú — 4 refinement từ research (ĐỀ XUẤT, CHƯA áp)
Chờ chủ dự án duyệt trước khi thành ADR chính thức. Nguồn: `docs/prior-art-research.md`.
1. Giữ bước edit code **đơn luồng**; chỉ song song hoá soát spec / điều tra / sinh test.
2. **Test/harness bất khả sửa** với con Fix bug (hàng rào cấu trúc cho "không chữa triệu chứng").
3. Bug DB thêm **kiểm-xung-đột ngữ nghĩa lúc ghi + temporal decay** ngoài fingerprint hash.
4. Đặt **kỳ vọng iOS thấp hơn số Python**; ưu tiên snapshot testing hơn tap toạ độ.
