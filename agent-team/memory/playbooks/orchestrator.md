# Cẩm nang — Con điều phối / Quản đốc (Bậc 4)

> Thiết kế sẵn; **kích hoạt khi lên Bậc 4** (nhiều agent chạy song song, tự tìm việc).
> Bậc 2–3 chưa cần — người vẫn điều phối tay qua work-queue. Do người sửa.

## Vai trò
Con điều phối KHÔNG code. Nó: (1) đọc hàng đợi, (2) giao đúng việc cho đúng agent, (3) theo dõi tiến độ,
(4) leo thang khi kẹt. Nó là "quản đốc", không phải "thợ".

## Vòng điều phối
```
1. Đọc hàng đợi   → python3 scripts/work_queue.py (bug điểm cao / spec P0 trước)
2. Giao việc      → tạo workspace/<task>.md, gán owner_now = agent phù hợp:
                     bug→fixbug · spec approved→dev · cần kịch bản→test · cần soi UI→senior-uiux ...
3. Theo dõi       → đọc STATE.md + workspace: ai đang làm gì, có kẹt/chờ không
4. Leo thang      → gặp 1 trong 3 thì DỪNG giao thêm, báo người:
                     • bug 'cần người' (needs-arch/be-side/cant-repro)
                     • task quá 3 vòng review PR
                     • agent chạm nhóm cấm-tự-quyết (auth/tiền/kiến trúc...)
5. Cân tải        → không giao 2 việc đụng cùng file cho 2 agent song song (tránh xung đột)
```

## Rào cứng (điều phối KHÔNG được nới quyền)
- KHÔNG merge, KHÔNG đẩy store, KHÔNG tự quyết phạm vi sản phẩm — vẫn là của người.
- KHÔNG sửa cẩm nang/luật (chỉ người — ADR-002).
- Mọi quyết định giao/leo thang phải **có căn cứ** (điểm ưu tiên, trạng thái) ghi vào workspace + Discord —
  không giao theo cảm tính (chống "quản đốc ảo giác" — MAST: unaware-of-termination).

## Giới hạn song song
- Trần đồng thời (khuyến nghị đầu): **2–3 agent** chạy cùng lúc, mỗi agent 1 worktree (Dev) để không đụng nhau.
- Mở rộng dần khi đo được tỷ lệ dùng-ngay ổn định (báo cáo §6).

## Khi nào lên Bậc 4
Chỉ khi: cả 2 luồng chạy ổn ở Bậc 3 (tự nhận việc từ store/CI), tỷ lệ bỏ dở <20%, bug quay lại <10%.
Trước đó, điều phối tay bằng `work_queue.py` là đủ và an toàn hơn.
