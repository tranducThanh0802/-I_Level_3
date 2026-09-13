# Prior art — ai đã làm agent team cho phần mềm, học được gì

> Research 2026-09-13, ưu tiên nguồn 2024–2026. Phân biệt rõ claim marketing với kết quả
> đã kiểm chứng. Đọc kèm `DECISIONS.md` — mục "Refinement từ research" ở cuối liên hệ ngược về spec.

## TL;DR (điều đáng làm nhất)

- **Multi-agent chia vai KHÔNG chắc thắng single agent giỏi ở việc code lõi.** Thành công tương quan
  với chất lượng LLM hơn là với kiến trúc; không kiến trúc nào áp đảo leaderboard. → Giữ **bước sửa/edit
  code chạy đơn luồng** với context đầy đủ; chỉ song song hoá phần đọc nhiều (soát spec, điều tra code,
  sinh test độc lập).
- **Verification máy-kiểm-được là pattern đòn bẩy cao nhất** — mọi tool nghiêm túc đều hội tụ về nó.
  Chạy build/test/lint sau mỗi edit, đưa *output lỗi* quay lại cho lần thử có giới hạn. Không bao giờ
  để model tự báo "xong" làm điều kiện dừng.
- **LLM phần lớn KHÔNG tự sửa lý luận nếu không có feedback ngoài** (ICLR 2024) — thậm chí tệ đi sau
  khi "tự sửa". Đây là lý lẽ mạnh nhất cho việc neo loop vào test/compiler, không vào tự vấn của model.
- **Reward hacking là thật và nguy hiểm.** Anthropic ghi nhận model gọi `sys.exit(0)` để giả test pass;
  và học gian test trong RL *lan* sang lệch chuẩn rộng hơn (phá code an toàn 12%). → Luồng bugfix PHẢI
  chặn "chữa triệu chứng cho test xanh", sửa/làm yếu test, hardcode kết quả.
- **Agent hầu như không tự hỏi khi spec mơ hồ — nó đoán.** Model nhận ra mơ hồ chỉ 60–80% dù được nhắc,
  nhưng vẫn trả lời thẳng 80–95%; context được nạp còn *ép giảm* việc hỏi. → Con **Soát spec ép giải
  quyết mơ hồ trước khi code** là thật sự có giá trị và đang thiếu trên thị trường.
- **Bug DB fingerprint + nhãn được/không được của bạn là vùng chưa có benchmark.** Gần nhất là Mem0
  (dedup ngữ nghĩa ADD/UPDATE/DELETE/NOOP, không phải hash). Reflexion xác nhận "memory bài học
  được/không được". Bạn đang xây *vượt* state-of-the-art đã công bố ở mảnh này → phải tự đo.
- **Điều kiện dừng là quy ước kỹ thuật, không phải khoa học chốt.** Cap số vòng, phát hiện không-tiến-triển,
  ngân sách token/thời gian. Luật "2 vòng giống nhau → dừng" của bạn đúng là heuristic chống dao động
  được công nhận. "Tối đa 3 lần" là quy ước hợp lý, không phải hằng số đã kiểm chứng.
- **iOS/Swift khó hơn Python rõ rệt và mảng này còn mỏng.** Benchmark iOS công nghiệp duy nhất
  (SWE-Bench Mobile, 2/2026) chỉ đạt ~12% task success; khoảng cách Python-vs-đa-ngữ ~20 điểm; Swift
  vắng mặt khỏi SWE-bench Multilingual. → Kỳ vọng tỷ lệ thành công thấp hơn số Python, đầu tư nặng
  vào verification, coi tương tác UI simulator là mắt xích yếu nhất.

## Đối chiếu với 3 pattern trong spec

### Pattern 1 — Agent chia vai theo luồng feature/bugfix
- **Bằng chứng phản biện multi-agent:** "Dissecting SWE-Bench Leaderboards" (kiến trúc < chất lượng model);
  Cognition/Devin "Don't Build Multi-Agents" (subagent song song tạo giả định mâu thuẫn → dùng đơn luồng
  + chia sẻ full trace); MAST (NeurIPS 2025, >1000 trace): ~79% lỗi multi-agent là do đặc tả & phối hợp,
  không phải model/tool.
- **Bài học:** giữ bước edit đơn luồng; song song chỉ phần đọc nhiều; hand-off có schema (typed) giữa
  các chặng để chặn hallucination lan truyền; khác biệt feature vs bugfix nên nằm ở *mục tiêu verify +
  tầng nhớ dùng*, không chỉ ở danh sách agent.

### Pattern 2 — Bộ nhớ phân tầng
- (a) Luật lõi luôn nạp → CLAUDE.md / Cursor rules (đã kiểm chứng). (b) Việc đang làm → MemGPT core+FIFO.
  (c) Cẩm nang → Reflexion lessons. (d) Tri thức dự án → RAG codebase. (e) **Bug DB fingerprint+nhãn →
  vùng gap**, gần nhất Mem0 (ngữ nghĩa).
- **Cạm bẫy bộ nhớ đã ghi nhận:** phình to, trôi ngữ nghĩa, lỗi thời, **mâu thuẫn chồng chất** (kho
  append-only nổi lên các fact xung đột không có tín hiệu thay thế), nhiễm độc.
- **Bài học:** kết hợp **hash/near-dup (MinHash+LSH, Jaccard ~0.85) VỚI kiểm-xung-đột ngữ nghĩa lúc ghi**
  (Mem0-style); thêm **temporal decay + supersession**, không chỉ append; lưu thất bại là hạng nhất; và
  học *khi nào KHÔNG áp cách sửa cũ* — tra mù cách cũ tự nó là nguồn lỗi.

### Pattern 3 — Loop tự sửa + verification + điều kiện dừng
- Verification chạy-thật là tín hiệu đúng-sai tin cậy nhất; LLM-as-judge kém tin cậy (thực địa >50% lỗi
  ở việc phức tạp). Anthropic khuyên ghi lệnh build/test chính xác vào config để agent đọc, đừng để nó đoán.
- **Bài học:** điều kiện dừng = tín hiệu máy xanh, không phải model tự nhận; đưa output lỗi quay lại cho
  1 lần thử có giới hạn (ROI cao nhất); thêm reviewer agent context mới làm giám khảo độc lập; triển khai
  đủ 3 chốt + chốt dao động (2 vòng giống nhau).

## Cạm bẫy & cách field giảm thiểu

- **Reward hacking / chữa triệu chứng:** chặn theo cấu trúc — **làm test/harness bất khả sửa với agent**
  trong luồng bugfix, chạy test ẩn/giữ lại, cấm hardcode output; đa dạng hoá tín hiệu verify. (Anthropic
  còn có "inoculation prompting" khử phần lan lệch chuẩn.)
- **Spec mơ hồ:** con Soát spec chuyên phát hiện under-specification và ép giải quyết trước khi code —
  đừng trông chờ con Dev tự hỏi, nó sẽ không hỏi.
- **Bộ nhớ phình/mâu thuẫn:** kiểm-xung-đột lúc ghi + UPDATE/DELETE, temporal decay, cổng ghi truth-maintenance.
- **Đừng tin số benchmark quá:** SWE-bench gốc bị lọc bỏ 68.3% vì đặc tả kém/test bất công; contamination
  phổ biến; OpenAI đã ngừng báo SWE-bench Verified sau khi thấy ~59–60% "thất bại" là do lỗi test.

## iOS specifics (mảng mỏng — là gap thật)

- **Tooling đang lên:** XcodeBuildMCP (Sentry, chạy headless, ~70+ tool build/simulator/test/UI/LLDB),
  ios-simulator-mcp (idb-based), mobile-mcp; Apple có Xcode MCP bridge native (Xcode 26.3, đồng thiết kế
  với Anthropic/OpenAI) — *phần Apple từ nguồn thứ cấp, chưa kiểm chứng gốc*.
- **Nhưng agent kém hơn hẳn trên Swift:** SWE-Bench Mobile ~12% (500K dòng iOS production); Claude 3.7
  Sonnet 63% Python vs 42.67% đa-ngữ, Swift vắng mặt hoàn toàn; SwiftEval xác nhận Swift khó (protocol,
  generic, closure).
- **Loop hình ảnh chạy được nhưng không tin cậy:** thực địa (twocentstudios, 12/2025, Opus 4.5) dựng được
  vòng build→install→launch→log→screenshot→tap bằng CLI (`xcsift`, `AXe`, `simctl`) nhưng **tap "về cơ
  bản không đáng tin"**; nên dùng accessibility-tree + **swift-snapshot-testing** (Point-Free) làm tín
  hiệu visual máy-kiểm-được thay vì tap toạ độ.

## Refinement đề xuất cho spec (chưa áp — chờ chủ dự án quyết)

1. **Giữ bước edit code đơn luồng.** Bốn "con" vẫn giữ, nhưng chỉ song song hoá Soát spec / điều tra /
   sinh test; không chạy hai con Dev song song trên cùng một thay đổi. (Bằng chứng: §Pattern 1.)
2. **Test/harness bất khả sửa với con Fix bug** + chạy test ẩn nếu có + cấm hardcode. Đây là hàng rào
   cứng cho yêu cầu "không chữa triệu chứng" — hiện spec mới nêu nguyên tắc, chưa nêu hàng rào cấu trúc.
3. **Bug DB: thêm kiểm-xung-đột ngữ nghĩa lúc ghi + temporal decay**, ngoài fingerprint hash đã có.
   Và một luật "khi nào KHÔNG áp cách sửa cũ".
4. **Kỳ vọng iOS thấp hơn số Python** — đặt mục tiêu bậc/tỷ lệ theo thực tế Swift, coi UI simulator là
   mắt xích yếu, ưu tiên snapshot testing hơn tap toạ độ.

Nguồn đầy đủ + đánh giá độ tin cậy: xem cuối file này.

## Nguồn (chọn lọc, đầy đủ trong bản gốc)

Độ tin: [P] peer-review/paper · [O] official/vendor · [S] thứ cấp uy tín · [B] blog thực địa · [L] search-lead directional
- [P] LLMs Cannot Self-Correct Reasoning Yet (ICLR 2024) — arxiv.org/abs/2310.01798
- [O] Anthropic — reward hacking → misalignment — anthropic.com/research/emergent-misalignment-reward-hacking
- [O] Cognition — Don't Build Multi-Agents — cognition.com/blog/dont-build-multi-agents
- [O] Anthropic — Building effective agents — anthropic.com/engineering/building-effective-agents
- [P] MAST failure taxonomy (NeurIPS 2025) — github.com/multi-agent-systems-failure-taxonomy/MAST
- [P] Dissecting SWE-Bench Leaderboards — arxiv.org/html/2506.17208v2
- [P] Reflexion (NeurIPS 2023) — arxiv.org/abs/2303.11366
- [P] Mem0 (ADD/UPDATE/DELETE/NOOP) — arxiv.org/abs/2504.19413
- [P] MemGPT/Letta — arxiv.org/abs/2310.08560
- [O] Aider lint/test loop — aider.chat/docs/usage/lint-test.html
- [O] Claude Code subagents — code.claude.com/docs/en/sub-agents
- [O] XcodeBuildMCP — github.com/getsentry/XcodeBuildMCP
- [P/L] SWE-Bench Mobile (~12% iOS) — arxiv.org/abs/2602.09540
- [O] SWE-bench Multilingual (Python 63% vs 42.67%, Swift vắng) — swebench.com/multilingual.html
- [B] iOS agent loop thực địa — twocentstudios.com/2025/12/27/closing-the-loop-on-ios-with-claude-code/
