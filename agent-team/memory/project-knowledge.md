# Tri thức dự án

> Nạp **theo file đang chạm tới** (không nạp hết mọi lúc). Do **người** sửa, agent không ghi.
> Chứa: cấu trúc, chuẩn code, quyết định cũ và lý do — để agent code "giống code xung quanh".
>
> **CÁCH ĐIỀN:** mỗi mục có 🔹 *cần điền* · 💡 *dùng cho* · 📍 *tìm ở đâu* · _ví dụ_. Thay `<...>` bằng
> giá trị thật của repo. Mục đánh dấu ✅ là mặc định từ skill `apero-review` — **xác nhận lại** cho khớp.
> Điền tới đâu, xoá dòng hướng dẫn tới đó cũng được. **Đừng để `<...>` sót lại** — agent thấy trống sẽ hỏi.

---

## 1. Kiến trúc

- ✅ Clean Architecture · DI bằng **Factory** · điều hướng **Coordinator**. *(xác nhận lại)*
- ✅ Ranh giới: **ViewModel không gọi thẳng Repository** (đi qua UseCase). *(xác nhận lại)*
- 🔹 Các module chính + trách nhiệm: `<liệt kê>`
  💡 để agent biết đặt code mới vào đâu. 📍 xem cây thư mục `Sources/` hoặc `*.xcodeproj` groups.
  _Ví dụ: `Feature/Player` (màn phát), `Core/Network` (gọi API), `Core/Storage` (lưu local)._
- 🔹 Sơ đồ layer (Presentation / Domain / Data): `<mô tả ngắn hoặc link>`

## 2. Chuẩn code

- ✅ Cấm **force-unwrap** (`!`) / force-try ngoài chỗ được duyệt. *(apero-review bắt)*
- ✅ Cấm leak secret/khoá trong code.
- ✅ Cẩn thận **retain cycle** (`[weak self]`, delegate `weak`).
- ✅ ViewModel → Repository trực tiếp: cấm.
- 🔹 Quy ước đặt tên / tổ chức file / thứ tự thành viên: `<mô tả hoặc link style guide>`
  📍 hỏi lead, hoặc suy từ file mẫu tiêu biểu.
- 🔹 Chuẩn SwiftUI (Observation, cách khởi tạo & truyền dependency): `<...>` 📍 skill `swiftui-view-refactor`.
- 🔹 Chuẩn concurrency (Swift 6.2+): `<...>` 📍 skill `swift-concurrency-expert`.

## 3. Bốn trạng thái UI (bắt buộc mọi màn có dữ liệu)

`loading` · `rỗng (empty)` · `lỗi (error)` · `mất mạng (no connection)`.
Spec thiếu ≥3/4 → Soát spec trả lại. UI thiếu → Test/Senior UI/UX đánh trượt. *(không cần điền — luật cố định)*

## 4. Build / Test / Lint — MÁY KIỂM của loop (quan trọng nhất)

> Đây là "một lần máy kiểm" của mọi loop. Agent phải chạy đúng lệnh này, KHÔNG được đoán (research:
> ghi lệnh chính xác vào đây để agent đọc). Ghi kết quả THẬT, không tự thuật.

- 🔹 Workspace/Project + Scheme: `<App.xcworkspace>` / `<scheme>`
  📍 mở Xcode xem tên scheme; hoặc `xcodebuild -list`.
- 🔹 Lệnh **build**: `<...>`
  _Ví dụ: `set -o pipefail; xcodebuild build -workspace App.xcworkspace -scheme App -destination 'platform=iOS Simulator,name=iPhone 16,OS=latest' | xcsift --Werror`_
- 🔹 Lệnh **test** + cách lấy kết quả thật: `<...>`
  _Ví dụ: `xcodebuild test -workspace App.xcworkspace -scheme App -destination '...' | xcsift -c`_
- 🔹 **Lint**: `<...>` _Ví dụ: `swiftlint lint --strict --reporter json`_ · 📍 file `.swiftlint.yml` ở đâu?
- 🔹 Simulator ghim (để snapshot ổn định): `<vd: iPhone 16, iOS 18.x>`
- 🔹 Snapshot/visual test: `<có dùng swift-snapshot-testing? baseline ở đâu?>`
- 💡 Chưa cài `xcsift`/`swiftlint`? `brew install xcsift swiftlint`.

## 5. Bàn giao — quay video + ảnh trước/sau

- 🔹 Lệnh quay video simulator: `<...>` _Ví dụ: `xcrun simctl io booted recordVideo --codec h264 out.mov`_
- 🔹 Ảnh chụp: `<...>` _Ví dụ: `xcrun simctl io booted screenshot before.png`_
- 💡 Điều khiển UI theo accessibility label: xem skill `ios-debugger-agent` / công cụ `AXe`.

## 6. Quy ước commit / PR

- ✅ Commit: `[IIP-XXX][Area]: <mô tả>` *(apero-review — xác nhận mã ticket đúng dự án)*
- 🔹 Template PR / nhãn / reviewer bắt buộc: `<...>` 📍 xem `.github/PULL_REQUEST_TEMPLATE.md` nếu có.

## 7. Backend (BE) — TUỲ LOẠI APP, có thể KHÔNG có

- 🔹 **Project này có BE không?** ☐ Có · ☐ Không (offline/local-only)
- Nếu **KHÔNG**: nguồn dữ liệu local là gì? `<CoreData / SwiftData / UserDefaults / file>`
  💡 luật "không tự đổi cấu trúc dữ liệu local" vẫn áp (đổi schema local phá app cũ khi update).
- Nếu **CÓ**:
  - 🔹 BE cùng team hay khác team? `<...>` 💡 quyết cách xử lý (core-rules §3).
  - 🔹 Docs BE (bản chính) ở đâu + cách phát hiện khi đổi: `<link>`
  - 🔹 Base URL / môi trường (dev/staging/prod) + cách xác thực: `<...>`

## 8. Nguồn việc luồng bugfix

- 🔹 **Crash từ store** lấy ở đâu? `<Firebase Crashlytics / Sentry / App Store Connect>`
  💡 để con Fix bug nạp crash + tính fingerprint. 📍 hỏi team hạ tầng.
  _Gợi ý: Crashlytics → BigQuery export cho query có cấu trúc; Sentry có REST API/webhook._
- 🔹 **CI / build đỏ** ở đâu, agent đọc trạng thái kiểu gì? `<GitHub Actions / Bitrise / ...>`
- 🔹 Kênh **bug tester / user report**: `<Jira / Asana / Linear / Slack ...>`

## 9. Quyết định cũ theo vùng code (để agent đừng "sửa" nhầm)

> Những chỗ "trông sai nhưng cố ý" — ghi lại kèm lý do.
- 🔹 `<file/vùng>` — `<vì sao cố tình như vậy>`
  _Ví dụ: `LegacyPlayer.swift` giữ API cũ vì còn màn X phụ thuộc — đừng refactor khi chưa gỡ X._
