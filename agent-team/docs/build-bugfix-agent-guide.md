# Hướng dẫn dựng con Fix bug cho iOS (thực hành)

> Research 2026-09-13. Đây là "how-to" cụ thể để dựng agent ĐẦU TIÊN: con Fix bug cho codebase
> iOS/Swift bằng Claude Code subagents. Kèm lệnh/snippet cụ thể. Chỗ nào mong manh/chưa kiểm chứng
> đánh dấu **[FLAG]**. Đọc kèm `prior-art-research.md` (landscape) và `DECISIONS.md`.

## Phát hiện quan trọng nhất (đọc trước)

**Cạm bẫy deadlock:** nếu chặn cứng agent ghi vào mọi file test (để chống reward-hacking), thì chính
nó cũng không tạo được bài test chống tái phát → kẹt. **Giải pháp bắt buộc:** tách làm 2 subagent —
một con `test-author` chỉ được tạo file test MỚI (chưa tồn tại), một con `bugfix-agent` bị chặn ghi
MỌI file test trong lúc sửa. Đây là thứ khiến "sửa test cho xanh" trở nên bất khả về mặt cấu trúc.

---

## 1. Thiết lập subagent Claude Code

Subagent = file Markdown có YAML frontmatter, đặt trong `.claude/agents/` (phạm vi dự án) hoặc
`~/.claude/agents/` (phạm vi người dùng). Phần thân dưới frontmatter là system prompt.

### 1.1 `.claude/agents/bugfix-agent.md`

```markdown
---
name: bugfix-agent
description: >
  Nhận crash iOS (stack trace), dedup theo bug DB, tìm ROOT CAUSE, sửa tối thiểu,
  viết test chống tái phát (fail-trước / pass-sau), mở PR kèm video + ảnh trước/sau.
tools: Read, Grep, Glob, Bash, Edit, Write, WebFetch
model: opus
maxTurns: 40
memory: project
isolation: worktree
---

Bạn là kỹ sư sửa bug cho app iOS (Clean Architecture / Factory DI / Coordinator, XCTest).
MỤC TIÊU KHÔNG BAO GIỜ ĐỔI qua các lần thử:
"Làm cho crash mà test chống tái phát tái hiện KHÔNG còn xảy ra, bằng cách sửa NGUYÊN NHÂN GỐC
trong code production."

LUẬT CỨNG:
- KHÔNG sửa/xoá/tắt/làm yếu/skip bất kỳ file nào dưới Tests/, *Tests.swift, snapshot, CI config.
  Bài test chống tái phát là hợp đồng; bạn làm code PRODUCTION thoả nó.
- Ưu tiên thay đổi nhỏ nhất loại bỏ nguyên nhân gốc. KHÔNG dập triệu chứng (thêm ?/try?/guard
  return để giấu lỗi).
- Báo cáo: fingerprint, giả thuyết nguyên nhân gốc + bằng chứng, diff, các tín hiệu verify.
  Không sửa được trong ngân sách → DỪNG, bàn giao cho người kèm phát hiện.
```

### 1.2 Các trường frontmatter quan trọng (từ docs chính thức)

| Trường | Dùng |
|---|---|
| `name` | id chữ-thường-gạch-nối, không `:` |
| `description` | khi nào giao việc cho nó (điều khiển auto-invoke) |
| `tools` | **allowlist** — có thì chỉ được dùng đúng các tool này; bỏ trống = kế thừa tất cả |
| `disallowedTools` | denylist, trừ đi khỏi tập tool |
| `model` | `sonnet`/`opus`/`haiku`/`fable`/id đầy đủ/`inherit` |
| `permissionMode` | `default`/`acceptEdits`/`plan`/... |
| `maxTurns` | số lượt tối đa trước khi dừng (điều kiện dừng mỗi lần chạy) |
| `memory` | `user`/`project`/`local` — scratch bền qua các lần chạy |
| `isolation` | `worktree` → mỗi lần chạy có git worktree riêng, giữ cây chính sạch |

**[FLAG]** Subagent chạy nền bị giới hạn tập tool cố định bất kể frontmatter → chạy con Fix bug
ở foreground khi nó cần Edit/Write tự do.

### 1.3 Hook CHẶN sửa file test (chống reward-hacking)

Đây là hàng rào chịu lực. `PreToolUse` chạy trước mỗi tool call và có quyền phủ quyết. Đăng ký trong
`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write|NotebookEdit",
        "hooks": [ { "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-tests.sh" } ] }
    ]
  }
}
```

`.claude/hooks/protect-tests.sh` — từ chối ghi vào file test/snapshot/CI:

```bash
#!/bin/bash
input=$(cat)
path=$(jq -r '.tool_input.file_path // empty' <<<"$input")
case "$path" in
  *Tests.swift|*Test.swift|*Spec.swift|*/Tests/*|*/__Snapshots__/*|\
  */.github/workflows/*|*/fastlane/*|*Package.swift)
    jq -n '{hookSpecificOutput:{hookEventName:"PreToolUse",
      permissionDecision:"deny",
      permissionDecisionReason:"Chặn: bug-fix agent không được sửa test/CI. Hãy sửa code production để thoả test."}}'
    exit 0 ;;
esac
exit 0
```

- Deny bằng JSON: in `hookSpecificOutput` với `permissionDecision:"deny"` + `exit 0`. (Deny bằng
  exit code 2 cũng chặn; stderr thành lý do.)
- Nhiều hook cùng khớp → quyết định **hạn chế nhất thắng** (`deny > ask > allow`).
- **[FLAG] Nút thắt:** deny chặn cả việc con tạo test mới → phải tách `test-author` (chỉ tạo file
  test CHƯA tồn tại, kiểm bằng `test -e`) khỏi `bugfix-agent` (khoá toàn bộ test khi sửa).
- Hook phụ trên `Bash`: chặn lệnh khớp `xcodebuild.*-skip-testing`, `rm .*Tests`, sửa `.pbxproj` gỡ test target.

---

## 2. Build/test/lint làm tín hiệu máy-kiểm-được

Agent phải đọc tín hiệu **có cấu trúc, ít token** — không đọc log xcodebuild thô.

### 2.1 Build & test parseable — dùng `xcsift`

`xcbeautify`/`xcpretty` làm đẹp cho người; `xcsift` chuyển output xcodebuild thành **JSON/TOON cho agent**.

```bash
brew install xcsift
set -o pipefail   # BẮT BUỘC, nếu không pipe giấu mất exit code

xcodebuild build -workspace App.xcworkspace -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=latest' \
  2>&1 | xcsift --Werror --exit-on-failure

xcodebuild test -workspace App.xcworkspace -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=latest' \
  -enableCodeCoverage YES -resultBundlePath build/Result.xcresult \
  2>&1 | xcsift -c --coverage-details
```

- Chạy nhanh 1 test đang fail trong loop: `-only-testing:AppTests/CrashReproTests/test_repro_<fp>`.
- **Thay thế:** `XcodeBuildMCP` (~81 tool: build/test/boot sim/record video/screenshot). **[FLAG]** Với
  tín hiệu pass/fail thuần thì `xcodebuild | xcsift` đơn giản & xác định hơn; dùng XcodeBuildMCP khi
  cần điều khiển simulator tương tác. Đừng chạy cả hai làm nguồn chân lý — chọn một cổng.

### 2.2 Lint — SwiftLint
```bash
swiftlint lint --strict --reporter json   # --strict biến warning thành fail → cổng nhị phân sạch
```

### 2.3 Visual regression — swift-snapshot-testing
- Ghi baseline (người duyệt) 1 lần, commit vào `__Snapshots__/`. Trong loop chỉ chạy compare (hook
  đã chặn ghi `__Snapshots__/` nên agent không thể tự tạo baseline để ép pass).
- **[FLAG]** Snapshot test hay flaky theo Xcode/OS/scale. Ghim đúng 1 simulator + OS; coi visual là
  tín hiệu **tư vấn** lúc đầu, chưa phải cổng cứng, cho tới khi baseline ổn định.

### 2.4 Video + ảnh trước/sau (cho PR)
```bash
xcrun simctl boot "iPhone 16"
xcrun simctl io booted recordVideo --codec h264 --force repro.mov & REC=$!
# ... tái hiện / chạy UI test ...
kill -INT $REC
xcrun simctl io booted screenshot before.png
xcrun simctl io booted screenshot after.png
```
- Điều khiển UI theo accessibility label (không phải toạ độ): `AXe` (`brew install cameroncooke/axe/axe`).
  **[FLAG]** AXe dùng API accessibility **riêng tư** của Apple → chỉ local/CI, dễ vỡ khi Xcode lên đời;
  ưu tiên **XCUITest** tái hiện crash khi có thể (ổn định, nằm trong repo — nhưng bị hook khoá sau khi tạo).

---

## 3. Lấy crash & fingerprint

### 3.1 Lấy crash
- **Firebase Crashlytics → BigQuery export** (khuyến nghị nếu Apero dùng Crashlytics): query SQL crash
  thô — đúng nguồn có cấu trúc cho agent. Trường quan trọng: `issue_id`, `error_type` (FATAL/NON_FATAL/ANR),
  `blame_frame{blamed,symbol,file,line,library,offset}` (Crashlytics đã chọn sẵn frame nghi phạm),
  `exceptions`, `threads.frames`.
- **Sentry**: grouping mặc định = stacktrace + exception + message; override bằng `fingerprint`. Có REST API/webhook.
- **[FLAG] App Store Connect crash API**: hạn chế, chỉ dùng bổ trợ.

### 3.2 Công thức fingerprint (khoá dedup ổn định)
```
fingerprint = sha1(
    exception_type
  + "|" + normalized_top_app_frame_symbol   # frame đầu tiên thuộc MODULE APP (bỏ frame hệ thống)
  + "|" + enclosing_type_and_method          # vd "CheckoutViewModel.applyCoupon(_:)"
)
```
Quy tắc giữ ổn định: bỏ frame hệ thống (UIKit/SwiftUI/Foundation...), neo vào frame đầu trong module
app (dùng `blame_frame` của Crashlytics); chuẩn hoá symbol (bỏ offset, địa chỉ, `closure #3`, **số dòng**);
lấy exception type nhưng KHÔNG lấy message đầy đủ (chứa giá trị động).
Lưu `{fingerprint, issue_id, first_seen, last_seen, status, pr_url}`; khi nạp: fingerprint đã có &&
status ∈ {fixed, in-progress} → **skip (dedup)**; ngược lại tạo việc.

---

## 4. Nguyên nhân gốc vs triệu chứng & bài test

### 4.1 Ép agent về nguyên nhân gốc
1. **Hợp đồng prompt:** nêu giả thuyết nguyên nhân gốc + bằng chứng TRƯỚC khi sửa; fix chỉ chặn triệu
   chứng tại chỗ crash (thêm ?/try?/guard else return rỗng/if let nuốt lỗi) → bị từ chối. Trace ngược
   từ `blame_frame` tới nơi sinh ra giá trị xấu.
2. **Kiểm bán kính ảnh hưởng:** Grep các call site khác của hàm crash, giải thích fix đúng cho tất cả.
3. **Hook chống anti-pattern:** dùng skill apero-review / SwiftLint custom rule gắn cờ `try?`, `as!`,
   force-unwrap, `fatalError` mới trong diff.
4. **Hai pha:** tái hiện trước (viết test fail), sửa sau.

### 4.2 Test fail-trước / pass-sau
- `test-author` viết test tái hiện đúng input crash, assert hành vi ĐÚNG (không crash + kết quả mong đợi).
- **Máy kiểm tính "fail-trước":** chạy test mới trên commit CHƯA sửa → phải FAIL. Pass trên code chưa
  sửa nghĩa là test không phủ đúng bug → từ chối, viết lại. (`git stash` fix → chạy → assert exit≠0 →
  áp fix → chạy → assert exit==0.)
- Đặt tên test theo fingerprint: `test_repro_<fp8>()` để nối crash → test.

### 4.3 Chống test-gaming
- Hook deny (1.3) khiến sửa test/snapshot/CI bất khả trong pha sửa — hàng rào chính.
- Kiểm test không tầm thường: từ chối test không assert, `XCTAssertTrue(true)`, `XCTSkip`, hoặc assert
  không liên quan crash.
- **Giữ mục tiêu bất biến** qua các lần thử: steer luôn là "sửa nguyên nhân gốc để test đã-commit pass",
  KHÔNG BAO GIỜ là "làm cho test xanh" — vế sau chính là drift đẻ ra reward-hacking.

---

## 5. Loop verification + điều kiện dừng

Nguyên tắc: tách **mục tiêu** (nêu một lần, bất biến) khỏi **steer** (feedback mỗi vòng). Loop giám sát
giữ giới hạn xuyên-lần-chạy; giữ mục tiêu cố định để agent tối ưu sản phẩm, không tối ưu cái đồng hồ đo.

### 5.1 File trạng thái (resume được) — `.bugfix/state/<fp>.json`
```json
{ "fingerprint":"a1b2c3d4",
  "goal":"Fix root cause so test_repro_a1b2c3d4 passes; production code only.",
  "phase":"fixing", "iteration":2, "max_iterations":3, "budget_usd_remaining":4.10,
  "last_signals":{"build":"pass","unit":"fail","regression":"fail","lint":"pass","snapshot":"pass"},
  "last_diff_sha":"9f8e...", "prev_diff_sha":"9f8e...", "history":[], "terminal":null }
```

### 5.2 Loop (pseudo)
```
load state (or init from crash)                 # resume được
if fingerprint in bug_db and status in {fixed,in-progress}: STOP "dedup"

PHA reproduce:
  test-author viết test_repro_<fp>              # hook chỉ cho tạo file test MỚI
  chạy test trên commit BASE -> PHẢI FAIL       # không thì STOP "test-does-not-repro"
  git add + commit test                          # giờ bị hook khoá

PHA fix (loop):
  while true:
    iteration += 1
    if iteration > max_iterations: STOP "max-retries"     # 3
    if budget <= 0: STOP "budget"
    bugfix-agent chỉ sửa code PRODUCTION          # ghi test/CI bị DENY
    signals = {build, lint, regression(-only test_repro), unit(full suite), snapshot(advisory)}
    diff_sha = sha1(git diff)
    if diff_sha == prev_diff_sha: STOP "no-progress"      # 2 vòng giống nhau
    prev_diff_sha = diff_sha; persist(state)               # ghi sau mỗi vòng
    if all(build,lint,regression,unit == pass): break -> PHA ship
    else: steer = CHỈ các tín hiệu fail            # KHÔNG nhắc lại goal

PHA ship:
  record video + ảnh trước/sau (simctl/AXe)
  mở PR (fix + test + media); bug_db status=in-progress, pr_url
  STOP "success -> human review"
```

### 5.3 Điều kiện dừng (đều máy-kiểm-được)
- **max-retries**: iteration > 3.
- **budget**: budget ≤ 0 (đồng bộ với `maxTurns`).
- **no-progress**: 2 vòng liền cùng diff → dừng.
- **test-does-not-repro**: test mới pass trên base → dừng (test dởm).
- **success**: build+lint+regression+full-suite xanh → mở PR, giao người.
- Mọi nhánh ghi lý do terminal vào state trước khi thoát → resume không lặp pha đã xong.

---

## 6. Kế hoạch tuần 1 — lát cắt dọc mỏng ("bậc 1: một con, một bước, gọi tay")

Mục tiêu tuần 1: agent **gọi tay** nhận MỘT crash đã biết (dán stack trace đã symbolicate) và tạo ra
PR có test fail-trước/pass-sau + fix + media, cho MỘT fingerprint. Chưa auto-ingest, chưa dedup DB —
hardcode một crash.

- **Ngày 1–2 — Scaffold & hàng rào:** thêm `bugfix-agent.md` + `test-author.md` (tách); thêm
  `protect-tests.sh` + đăng ký PreToolUse; hook Bash chặn `-skip-testing`/gỡ test target.
  *Nghiệm thu:* `echo '{"tool_input":{"file_path":".../FooTests.swift"}}' | ./protect-tests.sh` chứa
  `"permissionDecision":"deny"`.
- **Ngày 2–3 — Bộ tín hiệu:** `brew install xcsift swiftlint`; viết `scripts/signals.sh` chạy
  build/test/lint qua `xcodebuild | xcsift` (`set -o pipefail`), emit 1 JSON `{build,unit,lint}`.
  *Nghiệm thu:* build cố tình hỏng → exit≠0 & `build=="fail"`; sạch → all pass.
- **Ngày 3 — Chứng minh reproduce-first:** chọn 1 crash thật từ Crashlytics, tính fingerprint tay;
  `test-author` viết `test_repro_<fp>`; chạy trên commit chưa sửa → xác nhận FAIL.
- **Ngày 4 — Loop sửa (gọi tay):** chạy `bugfix-agent` tay, `signals.sh` làm checker; cap 3 vòng;
  ghi `.bugfix/state/<fp>.json` mỗi vòng. *Nghiệm thu:* `git diff --name-only` không có `Tests/`/CI;
  `test_repro_<fp>` pass; full suite xanh; state terminal `success` ≤3 vòng.
- **Ngày 5 — Media + PR + bàn giao:** `scripts/media.sh` boot sim ghim, `recordVideo`+`before/after.png`;
  `gh pr create` kèm fix+test+media, body có fingerprint + giả thuyết nguyên nhân + bảng tín hiệu.
  *Nghiệm thu end-to-end:* 1 lệnh tạo ra (1) branch diff không đụng test/CI, (2) test_repro pass (đã
  fail ở base), (3) full suite xanh + lint --strict, (4) PR URL có .mov + 2 .png, (5) state `terminal:"success"`.

Hoãn sang tuần 2+: tự động ingest crash (BigQuery/Sentry), dedup DB thật + dịch vụ fingerprint,
visual regression làm cổng cứng, xếp hàng nhiều crash.

---

## Nguồn (chọn lọc)
- Claude Code — Subagents: code.claude.com/docs/en/sub-agents (chính thức)
- Claude Code — Hooks guide & reference: code.claude.com/docs/en/hooks-guide , /hooks (chính thức)
- xcsift: github.com/ldomaradzki/xcsift · Tuist "Teaching AI to Read Xcode Builds"
- XcodeBuildMCP: github.com/cameroncooke/XcodeBuildMCP · AXe: github.com/cameroncooke/AXe
- swift-snapshot-testing: github.com/pointfreeco/swift-snapshot-testing
- simctl video/screenshot: sarunw.com/posts/take-screenshot-and-record-video-in-ios-simulator
- Crashlytics BigQuery export + schema + grouping: firebase.google.com/docs/crashlytics
- Sentry fingerprinting: docs.sentry.io (SDK Fingerprinting)
- Loop engineering / chống reward-hacking: dev.to "Loop Engineering", todatabeyond.substack.com

### Nhắc lại các [FLAG] độ tin cậy
- **AXe** = API riêng tư; chỉ local/CI, dễ vỡ theo Xcode — ưu tiên XCUITest.
- **swift-snapshot-testing** = flaky; ghim 1 simulator, để advisory tới khi baseline ổn.
- **App Store Connect crash API** = hạn chế; ưu tiên Crashlytics-BigQuery hoặc Sentry.
- **XcodeBuildMCP vs xcsift** = đừng chạy cả hai làm cổng; xcsift đơn giản/xác định hơn.
- **Hook chặn test** = deny chặn cả việc agent tự tạo test → PHẢI tách test-author (chỉ file mới)
  khỏi pha fix (khoá toàn bộ), không thì loop deadlock.
