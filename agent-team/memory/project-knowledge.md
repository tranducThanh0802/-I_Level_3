# Tri thức dự án

> Nạp **theo file đang chạm tới** (không nạp hết mọi lúc). Do **người** sửa, agent không ghi.
> Chứa: cấu trúc, chuẩn code, quyết định cũ và lý do — thứ agent cần biết để code "giống code xung quanh".
>
> ⚠️ File này đang là KHUNG. Phần đánh dấu `TODO` cần người điền theo codebase iOS thật của Apero.
> Mấy mục đã điền lấy từ skill `apero-review` sẵn có — kiểm lại cho khớp thực tế trước khi dựa vào.

## Kiến trúc (từ apero-review skill — xác nhận lại)

- Clean Architecture, DI bằng **Factory**, điều hướng bằng **Coordinator**.
- Ranh giới bắt buộc: **ViewModel không gọi thẳng Repository** (đi qua UseCase/tầng trung gian).
- TODO: vẽ sơ đồ layer thật (Presentation / Domain / Data) + module boundaries.
- TODO: liệt kê các module chính và trách nhiệm mỗi module.

## Chuẩn code (HIGH-risk pattern — apero-review bắt)

- Cấm **force-unwrap** (`!`) và force-try ngoài chỗ được duyệt.
- Cấm leak secret/khoá trong code.
- Cẩn thận **retain cycle** (closure `[weak self]`, delegate `weak`).
- Cấm ViewModel → Repository trực tiếp (xem trên).
- TODO: quy ước đặt tên, tổ chức file, thứ tự thành viên trong type.
- TODO: chuẩn SwiftUI (Observation, cách khởi tạo & truyền dependency — xem skill swiftui-view-refactor).
- TODO: chuẩn concurrency (Swift 6.2+, xem skill swift-concurrency-expert).

## Bốn trạng thái UI bắt buộc (mọi màn có dữ liệu)

`loading` · `rỗng (empty)` · `lỗi (error)` · `mất mạng (no connection)`.
Spec thiếu ≥3 trong 4 → Soát spec trả lại. UI thiếu → Test đánh trượt.

## Build / test / lint (máy kiểm của loop)

- TODO: lệnh build chuẩn (xcodebuild / scheme / config).
- TODO: lệnh chạy test (XCTest / test plan) và cách lấy kết quả THẬT (không tự thuật).
- TODO: lint (SwiftLint config ở đâu, rule nào chặn merge).
- TODO: cách quay video simulator + chụp ảnh trước/sau cho bàn giao (xem skill ios-debugger-agent).

## Quy ước commit / PR

- Commit: `[IIP-XXX][Area]: <mô tả>` (từ apero-review).
- TODO: template PR, nhãn, reviewer bắt buộc.

## CI / nguồn việc luồng bugfix

- TODO: crash từ store lấy ở đâu (Firebase Crashlytics? App Store Connect? SensorTower MCP?).
- TODO: build đỏ / CI ở đâu, cách agent đọc được trạng thái.
- TODO: kênh bug tester / user report (Jira/Asana/Linear? MCP nào?).

## Backend (BE) — TUỲ LOẠI APP, có thể KHÔNG có

- **Project này có BE không?** ☐ Có · ☐ Không (app offline/local-only)
- Nếu KHÔNG: bỏ qua phần BE ở core-rules §3; chỉ giữ luật "không tự đổi cấu trúc dữ liệu lưu local".
  Nguồn dữ liệu local là gì (CoreData / SwiftData / UserDefaults / file)? → TODO điền.
- Nếu CÓ:
  - TODO: BE cùng team hay team khác? (xem core-rules §3).
  - TODO: docs BE (bản chính) nằm ở đâu, cách agent phát hiện khi nó đổi.
  - TODO: base URL / môi trường (dev/staging/prod), cách xác thực.

## Quyết định cũ theo vùng code

- TODO: những chỗ "trông sai nhưng cố ý" — ghi lại kèm lý do để agent đừng "sửa" nhầm.
