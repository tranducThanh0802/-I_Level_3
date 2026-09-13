# CLAUDE.md — context cho mọi phiên Claude / agent làm việc trên dự án này

> File này được nạp đầu mỗi phiên. Mục đích: bất kỳ phiên Claude nào (hoặc người mới)
> vào đây cũng hiểu đúng dự án là gì, đang ở đâu, và **không đi sai hướng** khi maintain.
> Đọc file này TRƯỚC, rồi mới đọc code.

## ⚡ Giao thức mở context mới (resume) — LÀM TRƯỚC KHI LÀM GÌ KHÁC

Mỗi khi mở một phiên/context mới trong project này, đọc theo đúng thứ tự rồi mới hành động:
1. **`agent-team/STATE.md`** — đang ở đâu, việc dở, đã xong gì (để KHÔNG làm lại).
2. **`CLAUDE.md` (file này) + `agent-team/memory/core-rules.md`** — luật.
3. **`agent-team/workspace/*.md`** — task còn dở, câu hỏi đang chờ.
4. Khi chạm bug: **`agent-team/memory/bugs/`** (fingerprint → có thể đã sửa rồi, đừng sửa lại).
5. Khi đổi/nghi ngờ hướng: **`agent-team/DECISIONS.md`** (đã quyết gì + vì sao).

**Cô lập giữa các project:** context CHỈ lấy từ file trong thư mục project HIỆN TẠI. Không dựa vào
trí nhớ chat của project khác. Mỗi project là một thư mục riêng (tạo bằng `init_project.py`) với
dữ liệu rỗng của riêng nó → không dính dữ liệu project cũ.

**Trước khi kết thúc phiên:** cập nhật `STATE.md` (việc dở, đã xong, việc kế tiếp, ghi chú bàn giao)
và `workspace/<task>.md`. Đây là "chỗ đứt" để phiên sau tiếp được — bỏ qua bước này là phiên sau làm lại.

## Dự án này là gì

Xây một **agent team** hỗ trợ quy trình phát triển iOS tại Apero. Quy trình con người **không đổi**:
PO vẫn là người, spec do người bàn giao. Agent team nhận spec đã bàn giao làm đầu vào và
chạy tới bước mở PR; **người duyệt và merge** — quyền này không bao giờ nới cho agent.

Nguồn gốc & yêu cầu đầy đủ: xem `agent-team/docs/original-spec.md` (bản gốc, không sửa).
Bản đọc nhanh + quyết định: `agent-team/PROJECT-CONTEXT.md`.

## Quy tắc bất di bất dịch (chi tiết ở agent-team/memory/core-rules.md)

1. **Agent không merge, không đẩy store.** Người làm hai việc này. Không nới quyền kể cả sau nhiều tháng chạy êm.
2. **Danh sách phải-dừng-hỏi**: tiền, đăng nhập, dữ liệu người dùng, quyền, xoá dữ liệu,
   đổi schema local, đổi API contract, thêm/đổi thư viện, đổi kiến trúc, sửa config/khoá/script
   phát hành, sửa file ngoài phạm vi task.
3. **BE là source of truth** — agent đọc, không sửa. Cấm đổi API contract để cho test xanh.
4. **"Xong" phải máy kiểm được** (build/test/lint/so ảnh). Agent tự khen không tính.
5. **Bàn giao đủ 3 thứ**: code + video luồng vừa sửa + ảnh trước/sau. Thiếu video = chưa xong.
6. **Chốt chặn loop**: >3 lần cùng bước → dừng; hết ngân sách → dừng; 2 vòng giống nhau → dừng.

## Bản đồ thư mục

```
agent-team/
├── PROJECT-CONTEXT.md          # đọc nhanh: mục tiêu, hiện trạng, roadmap, quyết định
├── DECISIONS.md                # nhật ký quyết định (ADR) — vì sao chọn thế này
├── docs/
│   └── original-spec.md        # yêu cầu gốc từ PO/chủ dự án, KHÔNG sửa
├── memory/                     # bộ nhớ 5 tầng (xem PROJECT-CONTEXT §Bộ nhớ)
│   ├── core-rules.md           # [nạp LUÔN] luật lõi — không-được-làm, chỗ phải hỏi
│   ├── project-knowledge.md    # [nạp theo file] cấu trúc, chuẩn code, quyết định cũ
│   └── bugs/                   # [nạp khi gặp bug giống] CSDL bug, có fingerprint + nhãn
└── logs/
    └── run-log.schema.md       # format runs.jsonl — đầu vào đánh giá & loop ngoài
```

## Ai được ghi vào đâu (QUAN TRỌNG — đừng phá)

- Agent **chỉ được ghi** vào: `memory/bugs/` và tầng "việc đang làm".
- `core-rules.md`, `project-knowledge.md`, cẩm nang/playbook: **chỉ người sửa**.
  Lý do: cho agent tự sửa luật của chính nó thì hai tuần sau không ai biết luật nào còn hiệu lực.
- Một luật chỉ nằm ở MỘT chỗ. Đừng copy luật sang file thứ hai — hai nơi sẽ lệch nhau.

## Trạng thái hiện tại

Xem mục "Hiện trạng" trong `PROJECT-CONTEXT.md` (cập nhật khi có tiến triển).
Tính tới lần cập nhật gần nhất: **đã dựng Bước 0** (hạ tầng bộ nhớ + log). Chưa dựng agent nào.

## Khi maintain, đừng đi sai hướng

- Trước khi đổi bất cứ gì trong `agent-team/`, đọc `DECISIONS.md` xem quyết định đó đã có lý do chưa.
- Bắt đầu từ **luồng fix bug**, không phải luồng feature (lý do trong PROJECT-CONTEXT).
- Đừng lấy nhóm việc khó nhất (kiến trúc giữa đường, race condition, spec mơ hồ) làm phép thử đầu tiên.
