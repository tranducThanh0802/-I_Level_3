# Bug cũ — bộ nhớ lỗi

> Nạp **khi gặp bug giống**. Đây là nơi agent Fix bug tra trước khi sửa, và ghi lại sau khi sửa.
> Agent **được ghi** vào đây (và vào "việc đang làm"). Không được ghi vào cẩm nang / tri thức dự án.

## Cách hoạt động

- Mỗi bug = một file `bug-<key>.md` trong thư mục này.
- **Trước khi sửa**: tra theo `fingerprint`. Trùng → cộng `count`, lấy lại cách sửa cũ thay vì mò lại.
- **Sau khi sửa**: cập nhật `outcome` (được / không được), kể cả cách đã thử mà thất bại.

## Ba đòi hỏi bắt buộc (mục 3 của spec)

1. **Khoá nhận trùng** (`fingerprint`) — cùng dấu hiệu lỗi thì cộng đếm, đừng mở bản ghi mới.
   Bộ đếm `count` chính là thứ về sau cho biết lỗi nào đã lặp ≥3 lần (đầu vào loop ngoài).
2. **Nhãn được/không được** (`outcome` trong mỗi `attempt`) — thiếu nhãn thì lần sau tra ra
   rồi lặp lại đúng cái sai cũ, mà nhìn ngoài lại tưởng hệ thống đang học.
3. **Dọn định kỳ** — gỡ bug gắn với code đã xoá hoặc chuẩn đã đổi.

## Schema mỗi bản ghi

```yaml
---
id: BUG-<n>                    # số thứ tự Jira-style, duy nhất & ổn định. Lấy số tiếp theo: scripts/new_bug.py
key: <slug ngắn, ổn định, dùng trong tên file>
fingerprint: <chuỗi nhận trùng: ví dụ "crash:NSInvalidArgument:PlayerViewModel.play:L142">
count: <số lần gặp>            # cộng mỗi lần gặp lại
severity: crash | high | medium | low
source: store | tester | user | ci
status: open | in-progress | needs-human | needs-arch | be-side | cant-repro | fixed | wontfix
assignee: <ai đang cầm; rỗng = chưa ai nhận>
stuck_reason: <nếu agent bó tay: vì sao — dùng cho cột "Cần người" ở bug board>
first_seen: <YYYY-MM-DD>
last_seen: <YYYY-MM-DD>
touched_files:                 # chỗ từng phải sửa (kể cả sửa tay)
  - <path>
---

# Nhóm trạng thái "Cần người" (agent DỪNG, người nhảy vào — đề bài §1 luồng bugfix):
#   needs-arch  = phải đổi kiến trúc mới hết
#   be-side     = lỗi phía BE (đóng gói bằng chứng gửi sang)
#   cant-repro  = thử 3 lần vẫn không tái hiện được
#   needs-human = lý do khác agent không tự quyết
# Người nhận: đổi assignee=tên mình, status=in-progress.

## Dấu hiệu
<log / stack trace rút gọn>

## Bước tái hiện
1. ...
2. ...

## Nguyên nhân gốc
<không phải triệu chứng — cái gì thật sự gây ra>

## Các lần thử
- [DATE] cách: <mô tả> → outcome: **được** / **không được** — <ghi chú>
- [DATE] cách: <...>     → outcome: ...

## Test chống tái phát
<tên test + nó chặn điều gì>
```

Xem `bug-EXAMPLE.md` cho một bản ghi mẫu.

## Phép thử bộ nhớ (mục 3)

Báo lại một bug đã từng sửa → agent phải tra ra được cách sửa cũ theo `fingerprint`.
Tra ra được = bộ nhớ thật sự dùng được. Không ra = mới chỉ có file cho có.
