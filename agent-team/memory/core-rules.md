# Luật lõi

> Nạp **luôn** cho mọi agent, mọi luồng. Giữ ngắn — dưới 2 trang.
> Một luật chỉ nằm ở đây, không lặp ở chỗ khác. Sửa luật → sửa ở đúng file này.

## 1. Không được tự quyết — gặp là DỪNG, hỏi người

Danh sách này áp cho **mọi** agent. Chạm vào bất kỳ mục nào thì dừng, đóng gói câu hỏi theo mẫu ở §4, chạy tiếp phần không liên quan trong lúc chờ.

- Tiền / thanh toán / in-app purchase
- Đăng nhập, xác thực, session, token
- Dữ liệu người dùng (đọc/ghi/xoá)
- Quyền truy cập, phân quyền
- Xoá dữ liệu (bất kỳ dạng nào)
- Đổi cấu trúc dữ liệu lưu trên máy (schema local, CoreData, UserDefaults keys, migration)
- Đổi API contract (field, endpoint, kiểu dữ liệu, mã lỗi)
- Thêm / đổi / gỡ thư viện (SPM, CocoaPods)
- Đổi kiến trúc (module, layer, luồng dữ liệu)
- Sửa cấu hình, khoá ký, hoặc script phát hành (fastlane, CI config, entitlements, Info.plist quan trọng)
- Sửa file **ngoài phạm vi task** đang làm

## 2. Không bao giờ nới quyền

- Agent **không merge**, **không đẩy lên store**. Kể cả khi mọi thứ đã chạy êm nhiều tháng.
- Người duyệt và merge. Người bấm phát hành.

## 3. Ranh giới BE

- BE là **bản chính (source of truth)**. Agent đọc, không sửa.
- Nếu BE team khác: phát hiện khi docs BE đổi → báo lên, không tự sửa gì phía BE.
- Nếu BE cùng team: **cấm** đổi API contract để cho test xanh. Bản app cũ trên máy người dùng vẫn phải chạy được với API hiện tại.
- Bug do phía BE: đóng gói bằng chứng gửi sang, bỏ khỏi hàng đợi, **không tự sửa**.

## 4. Mẫu câu hỏi gửi người (đọc-trả-lời trong 30 giây)

Cấm kiểu "chỗ này em không rõ, anh xem giúp". Mọi câu hỏi phải đủ:

```
Chỗ vướng:      <một câu>
Cách A:         <mô tả> → hệ quả: <...>
Cách B:         <mô tả> → hệ quả: <...>
Nghiêng về:     <A hoặc B> vì <lý do một câu>
Nếu quá hạn:    <việc agent sẽ tự làm nếu không ai trả lời>
```

Phân loại câu hỏi:
- **Chặn** → dừng đúng phần đó, chờ trả lời.
- **Đoán được** → ghi giả định vào PR, chạy tiếp.

## 5. Tiêu chí "xong" phải máy kiểm được

- "Xong" = build + test + lint xanh, hoặc so ảnh chụp, hoặc một agent khác đọc lại theo checklist.
- Agent **tự khen "đã xong" không tính**. Phải là thứ chạy được và trả về đúng/sai.
- Tiêu chí kiểu "làm cho đẹp" → không nhận, báo lên.

## 6. Bàn giao đủ 3 thứ, thiếu là chưa xong

1. Code (PR + mô tả)
2. Video quay màn hình luồng vừa sửa
3. Ảnh chụp trước và sau

## 7. Chốt chặn loop (không chạy vô hạn)

- Cùng một bước thử **quá 3 lần** → dừng.
- **Hết ngân sách thời gian** → dừng.
- **2 vòng liền ra kết quả y hệt** → dừng (đang xoay tại chỗ).

## 8. Ghi lại mọi lần chạy

Mọi lần chạy phải tra lại được: việc gì, mấy giờ, qua bước nào, hỏng ở đâu, người sửa tay
bao nhiêu, cuối cùng dùng được hay bỏ. Xem `logs/run-log.schema.md`.

Mỗi lần người phải sửa tay output của agent → ghi một dòng (đầu vào loop ngoài):

```
Loại: sai chuẩn / thiếu thông tin đầu vào / hiểu sai yêu cầu / sai logic
Cụ thể: <một câu>
```
