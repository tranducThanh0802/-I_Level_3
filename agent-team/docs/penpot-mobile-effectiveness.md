# Penpot cho mobile — số liệu thực tế & mức độ hiệu quả

> Research 2026-09-13. Tách rõ: (a) số cứng có nguồn, (b) cảm nhận review, (c) giai thoại, (d) marketing.
> Kết luận thẳng để không kỳ vọng lệch. Bổ trợ cho ADR-012.

## Kết luận thẳng (TL;DR)

Penpot là tool design mã nguồn mở **thật, đang lớn nhanh** (~1.5M user tự báo, ~60K★ GitHub — số cứng),
NHƯNG **gần như không có số liệu hiệu quả riêng cho mobile**. Số tồn tại hầu hết là *adoption chung*,
không phải bằng chứng "làm app iOS nhanh hơn nhờ Penpot".

- Adoption thật, tăng nhờ làn sóng rời Figma (Figma tăng giá 2025). Nhưng review **cỡ mẫu tí xíu**
  (G2 4.5/5 với 10 review; Capterra 4.0/5 với **1 review**) → tích cực nhưng yếu về mặt thống kê.
- Mobile: **làm được** UI + prototype mobile, và **xuất design tokens ra SwiftUI/Jetpack Compose** (điểm
  mạnh thật). NHƯNG: (a) **không có app mobile native** — thiết kế trên trình duyệt desktop; (b) **không
  sinh code màn hình mobile trực tiếp** (SwiftUI/Flutter); (c) **lag trên file lớn** — than phiền nhất.
- **Không có số before/after mobile** (tiết kiệm giờ/bug) từ team thật nào. Số tiết kiệm tiền là chung
  chung và chủ yếu từ marketing.

**Cho team iOS:** Penpot đáng tin ở mức *tool design + xuất token chi phí thấp*, còn "hiệu quả cho mobile"
thì **hứa hẹn nhưng bằng chứng mỏng**. → **Chạy pilot, tự đo số của mình**, đừng dựa vào ROI công bố (gần như không có).

## Bảng số cứng (kèm nguồn + cỡ mẫu)

| Chỉ số | Giá trị | Ngày | Loại |
|---|---|---|---|
| GitHub stars | **59,932** (live API) | 09/2026 | Cứng |
| Registered users | 250K → 400K → **1.5M** | 2023 → 2026 | Công ty tự báo (trừ 250K là báo chí) |
| Teams | 80,000+ | 06/2023 | Công ty tự báo |
| Self-host | >50% team tự host | 06/2023 | Công ty tự báo |
| Vốn gọi | $20M ($8M seed + $12M Series A) | 2022–23 | Cứng |
| Spike sau tin Adobe–Figma | +5,600% đăng ký/ngày | 09/2022 | Báo chí |
| Figma tăng giá | seat Pro $16→$20/mo (tới +33%) | 03/2025 | Cứng |
| G2 | 4.5/5 (**10 review**) | 2026 | Review, n nhỏ |
| Product Hunt | 4.8/5 (**8 review**) | 2026 | Review, n nhỏ |
| Capterra | 4.0/5 (**1 review**) | 2026 | Review, n=1 |
| AlternativeTo | 4.7/5 (**23 rating**) | 2026 | Cộng đồng, n nhỏ |

⚠️ Con "3,545 review / 4.5" trôi trên search **KHÔNG phải của Penpot** (là số tổng danh mục). Trang
Capterra của Penpot chỉ **1 review**.

## Mobile design → code: thực tế

- **Có:** xuất **design tokens** ra SwiftUI/Compose/Flutter (+ CSS/DTCG/JSON); panel Inspect đọc
  kích thước/màu/CSS — hữu ích nhưng **thiên web (CSS)**, không phải layout native.
- **KHÔNG có:** sinh "design → màn hình SwiftUI/Flutter" tự động. Thành viên community Penpot nói thẳng
  *"không có cách xuất trực tiếp sang Flutter"*; discussion #3032 vẫn là wishlist.
- → Pipeline mobile thật hôm nay = **tokens + tự code UI + panel inspect**, KHÔNG phải sinh màn tự động.
  Không có số "nhanh hơn X%" đáng tin.

## Hạn chế quan trọng cho team mobile

1. **Lag file lớn — than phiền #1.** Có case 2200×4600px chạy **0.5–5 fps, CPU 100% một nhân** (09/2024);
   UI "đứng vài giây" (10/2025); nặng với **500+ artboard / component lồng sâu** — đúng cảnh design system
   nhiều màn/trạng thái. Đang vá bằng renderer **Rust+WASM+WebGL (beta 2025–26)**, nhưng còn beta.
2. **Không app native; chỉ trình duyệt desktop.** Xem/sửa trên điện thoại/tablet yếu.
3. **Tính năng non hơn Figma:** component **variants mới có ~11/2025**; prototype thiếu logic điều kiện.
4. **Hệ sinh thái plugin nhỏ & mới** so với Figma → ít helper cho mobile.
5. **Import từ Figma không hoàn hảo** — auto-layout/prototype phức tạp phải làm lại tay (thuế di cư).
6. **Chi phí vận hành self-host** (Docker/K8s) — và một số than lag đến từ instance tự host thiếu tài nguyên.

## Case study / bên dùng có tên

- **GitLab** — case study công khai (design–dev communication), **không** kèm số mobile.
- Ghi nhận (directory, chưa audit): Microsoft, Mozilla, Google, S&P Global, Canonical, Locofy.ai.
- **Không tìm thấy** team làm app mobile nào công bố before/after với Penpot.

## Verdict cho team iOS + mức độ tin

Khả thi, nhưng mở mắt: kỳ vọng **không có screen→SwiftUI tự động**; **canh performance** nếu design system
lớn (test file thật trước); ít tutorial mobile hơn Figma; **không có app iPad/phone tốt**.

Độ tin dữ liệu: **thấp–trung bình.** (a) Số adoption/scale: tin được. (b) User count (1.5M): tự báo,
hợp lý nhưng chưa audit. (c) Review: thật nhưng **n quá nhỏ**. (d) **Hiệu quả/ROI mobile: gần như không có.**

**Khuyến nghị:** chạy **pilot 4–8 tuần** trên một feature iOS/một lát design-system thật, **tự đo** (thời
gian handoff, độ chính xác token→SwiftUI, performance ở quy mô của mình). ĐỪNG quyết dựa trên ROI mobile
công bố — nó gần như không tồn tại. Điểm mạnh thật của Penpot cho iOS: **chi phí, mở/self-host, design
tokens (SwiftUI/Compose), inspect thân thiện dev**. Điểm yếu thật: **lag file lớn, không app native,
không code-gen mobile, tính năng/plugin còn non.**

## Nguồn (chọn lọc)
- Cứng: api.github.com/repos/penpot/penpot (59,932★); techcrunch (250K user + Series A); crunchbase ($20M)
- Tự báo: community.penpot.app (400K/1.5M user, self-host >50%); penpot.app/blog (renderer Rust/WASM)
- Review: producthunt (4.8/8), capterra (4.0/1), alternativeto (4.7/23; comment "no Android/iOS")
- Hạn chế: github.com/penpot/penpot/issues/5063 (0.5–5fps), discussions/3032 (Flutter wishlist),
  community.penpot.app performance threads
- Case: peertube.kaleidos.net (GitLab × Penpot); appsruntheworld (directory bên dùng, chưa audit)
- Marketing (yếu nhất): blog so sánh chi phí ($255 vs $35, ~$20K/năm) — coi là minh hoạ, không phải đo thật
