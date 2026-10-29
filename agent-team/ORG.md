# ORG — Sơ đồ tổ chức "công ty agent"

> Mô hình: một CÔNG TY. **Bạn = CEO**, quyền cao nhất, duyệt mọi checkpoint và là người DUY NHẤT
> merge/phát hành (A4 + luật lõi #2). Mỗi vai trò nhỏ = 1 **skill** (`.claude/skills/<tên>/SKILL.md`),
> càng nhỏ & đơn nhiệm càng tốt → đóng gói, tái dùng, người khác copy là chạy (A8.1).
> Workflow = ghép nhiều skill qua các phòng (A1). Hình hài đóng gói = CLI `agent` (A8.2) — xem `scripts/agent_cli.py`.

## Nguyên tắc tổ chức
- **1 skill = 1 việc rõ ràng**, có đầu vào/đầu ra + điểm-dừng-hỏi-CEO nếu chạm luật lõi.
- **CEO duyệt ở checkpoint** (A4): skill KHÔNG tự quyết các điểm thuộc người (xem `memory/core-rules.md §1`).
  Khi dừng phải **báo ngay + nêu rõ quyết định cần + 2 phương án** (mẫu core-rules §4), không im lặng.
- **Máy chốt "xong"** (A4 điểm chặn thật): mọi feature qua `acceptance-gate` + reviewer độc lập ≠ author.
- **Phòng chỉ ghi vào phần của mình**; luật/playbook chỉ CEO (người) sửa.

## Sơ đồ

```
                               CEO  (BẠN — người)
                 duyệt checkpoint · merge · phát hành · ra đề (A4/A5/A8)
                                      │
   ┌───────────┬───────────┬─────────┼──────────┬───────────────┐
   ▼           ▼           ▼         ▼          ▼               ▼
 SẢN PHẨM   KỸ THUẬT    CHẤT LƯỢNG  TRI THỨC   VẬN HÀNH        (A7, điểm cộng)
 (Product)  (Eng)       (QA)        (Knowledge) (Ops)           Trợ lý-bản-sao
```

## Phòng ban & skill (vai trò)

### 1. SẢN PHẨM (Product) — biến ý muốn CEO thành spec máy-làm-được
- `research-idea`   — ý tưởng/đề bài → tìm hiểu, gom ràng buộc, câu hỏi cho CEO.
- `write-spec`      — viết spec; **đánh dấu rõ phần AI làm** (A1.1); liệt kê tiêu chí nghiệm thu.
- `review-spec`     — soát spec trước khi giao Kỹ thuật (đủ 4 trạng thái, không mơ hồ).

### 2. KỸ THUẬT (Engineering) — làm ra sản phẩm
- `make-acceptance` — spec → `acceptance/<feature>.md` (checklist từng mục + cách kiểm). **Trước khi code.**
- `implement`       — code 1 feature theo acceptance; mỗi mục điền bằng chứng.
- `fix-bug`         — sửa bug: tra `bug-memory` trước (đừng sửa lại), fingerprint, test hồi quy.

### 3. CHẤT LƯỢNG (QA) — gác cổng "xong", CEO không tự khen
- `independent-review` — phản biện ≠ author (context mới), nhiệm vụ BÁC BỎ, verdict PASS/FAIL.
- `ui-lint`            — máy chặn emoji-tofu / asset icon thiếu (`scripts/ui_lint.py`).
- `acceptance-gate`    — máy chặn "xong" nếu còn ô trống / reviewer chưa PASS (`scripts/acceptance_gate.py`).
- `port-oracle-tests`  — port test từ NGUỒN CHÂN LÝ (vd Android) làm oracle, không tự viết kỳ vọng.
- `regression-gate`    — không cho tụt baseline (`scripts/run_regression.py`).
- `security-scan`      — quét secret/PII trước khi lộ ra ngoài (`scripts/scan_secrets.py`).

### 4. TRI THỨC (Knowledge) — Knowledge Base có vòng lặp (A2)
- `knowledge-base`  — thêm/sửa/xóa/di chuyển/version QUY TẮC; biết dùng lúc nào, ở bước nào (A2.1/A2.2).
- `bug-memory`      — CSDL bug có fingerprint (gặp bug giống → có thể đã sửa).
- `outer-loop`      — retro; lỗi lặp ≥3 → đề xuất CEO sửa luật → chạy hồi quy → cập nhật baseline.

### 5. VẬN HÀNH (Ops) — chạy thật, đo được (A3/A6)
- `orchestrate`     — nhận 1 đầu việc → route qua các phòng theo đúng thứ tự (đây là WORKFLOW chính, A1).
- `work-queue`      — hàng đợi đầu việc (`scripts/work_queue.py`).
- `run-log`         — ghi mỗi lần chạy vào `runs.jsonl` (A3.2: ai/khi nào/qua bước nào/human_minutes).
- `automate-repeat` — khai danh mục việc lặp → auto ≥80%, có nhánh ngoại lệ (A6).

### 6. (A7 — điểm cộng) `my-replica` — bản sao 1:1 online của CEO qua AI Assistant.

## Luồng chuẩn 1 feature (workflow ghép skill — A1)
```
CEO ra đề → research-idea → write-spec → review-spec →[CEO duyệt]→ make-acceptance
  → implement → ui-lint + acceptance-gate(máy) → independent-review(≠author)
  →[CEO duyệt "đẹp/đồng ý"]→ run-log → outer-loop(retro) → CEO merge/phát hành
```
Mỗi mũi tên `[CEO duyệt]` = checkpoint A4 (dừng, báo rõ, chờ người). Xem `RUBRIC-MAP.md` để biết skill nào phủ tiêu chí nào.
