# Git/project hỗ trợ AI làm UI/UX — cho pipeline Penpot tự host + SwiftUI

> Research 2026-09-13. Ưu tiên mã nguồn mở, hợp hướng đã chốt (ADR-012: Penpot tự host + sinh SwiftUI
> theo component team + người duyệt visual). Đánh dấu rõ đóng/mở nguồn, bỏ hoang, và hype.

## Thông điệp cốt lõi (đọc trước)

Ràng buộc của team (Penpot **không phải Figma** + SwiftUI map component sẵn + người duyệt) là tổ hợp
**ít công cụ sẵn phục vụ**. Nên câu trả lời thực tế là **ghép pipeline từ vài mảnh tốt + LLM làm keo**,
KHÔNG phải "cài một sản phẩm là xong".

**Không tồn tại** công cụ Penpot → SwiftUI trực tiếp. Cầu nối thật sự = **design tokens** (penpot-export
→ JSON → hằng số Swift) + **LLM viết layout** theo component team + **snapshot test** làm cổng người duyệt.

## Top khuyến nghị cho team (hữu ích nhất trước)

| # | Repo | Vai trò | License | Chín? |
|---|---|---|---|---|
| 1 | **penpot/penpot** (thư mục `/mcp`, trước là penpot-mcp) | MCP chính thức: agent **đọc + tạo/sửa** design Penpot qua Plugin API | MPL-2.0 | Chính thức nhưng **experimental** (~497★) |
| 2 | **pointfreeco/swift-snapshot-testing** | Xương sống **cổng người duyệt visual**: sinh SwiftUI → render → so ảnh → người duyệt baseline | MIT | Chín, chuẩn de-facto (~4.3k★) |
| 3 | **penpot/penpot-export** | Xuất **tokens** màu/typography → CSS/SCSS/JSON (DTCG) → hằng số Swift. Cầu nối Penpot→SwiftUI *duy nhất đáng tin* | Apache-2.0 | Chính thức (~85★) |
| 4 | **Kỹ thuật DESIGN.md / skill** (voltagent/awesome-design-md; nextlevelbuilder/ui-ux-pro-max-skill có SwiftUI) | Nạp component library + luật design cho agent để nó sinh SwiftUI *đúng brand, đúng component* | MIT | Là *kỹ thuật*, không phải sao ★ |
| 5 | **swhitty/SwiftDraw** (+ bring-shrubbery/SVG-to-SwiftUI) | SVG icon/vector từ Penpot → SwiftUI | Zlib / Apache | Chín (~645★ / ~1.1k★) |
| 6 | **zcube/penpot-mcp-server** (dự phòng) | MCP cộng đồng đầy đủ nhất, 70+ tool tạo/sửa; hoặc **ancrz/penpot-mcp-server** (RPC, hợp self-host) | MIT / Apache | Sớm nhưng active |

## Theo 6 nhóm (gọn)

**1. Penpot + AI:** Agent **tạo/sửa được** design Penpot qua 3 đường: Plugin API (chính thức, cần
session), HTTP/RPC API (headless thật nhưng là **API nội bộ, không cam kết ổn định**), exporter Chromium
cho PNG/SVG. MCP chính thức + zcube/montevive/ancrz (cộng đồng).

**2. Design→code SwiftUI:**
- **bernaferrari/FigmaToCode** — GPL-3.0, ~5.2k★, **generator SwiftUI OSS tốt nhất** (nhưng là Figma, copyleft).
- **figma/code-connect** — MIT, **có SDK SwiftUI**, map component Figma↔code thật. *Penpot KHÔNG có tương đương.*
- Đóng nguồn/thương mại: **Anima** (SwiftUI đáng tin nhất nhưng trả phí), **Locofy/DhiWise-Rocket.new**
  (mạnh về web/RN, SwiftUI yếu/đã hạ ưu tiên). Không giúp Penpot.

**3. Sinh UI từ prompt/ảnh:** Hầu hết **chỉ ra web** (React/HTML). `abi/screenshot-to-code` (MIT, ~78.7k★)
và `wandb/openui` (Apache) — **không có SwiftUI**. `tldraw/make-real` **đã archive**. Ra SwiftUI thì đóng
nguồn (Anima, Compot) hoặc chỉ nghiên cứu (Apple **UICoder** — chứng minh khả thi, không xài được).

**4. MCP cho design tool:** Figma Dev Mode MCP (chính thức, hosted, đóng); **GLips/Figma-Context-MCP**
(MIT, ~15.8k★, cộng đồng phổ biến nhất, không cần Dev seat); Penpot MCP (mục 1); Sketch MCP (mới).

**5. iOS/SwiftUI:** **SwiftDraw** + **bring-shrubbery/SVG-to-SwiftUI** cho SVG. **swift-snapshot-testing**
cho vòng AI→snapshot→diff→duyệt. **exyte/Macaw đã DEPRECATED — đừng dùng.** Không có generator ảnh→SwiftUI
OSS chín nào; mấy cái iOS "screenshot→SwiftUI" là wrapper GPT đóng — coi là hype.

**6. Agent/framework design:** `superdesigndev/superdesign` (MIT, ~7k★) nhưng **ra React/Tailwind, không
SwiftUI**. `voltagent/awesome-design-md` (kỹ thuật DESIGN.md). `nextlevelbuilder/ui-ux-pro-max-skill`
(MIT, có luật SwiftUI — hiếm; **sao ★ khó tin, phải thử tay**).

## Khoảng trống (đừng kỳ vọng quá)

1. **Penpot → SwiftUI trực tiếp: KHÔNG có.** Cầu nối = tokens + LLM.
2. Claim "Penpot xuất token SwiftUI/Compose/Flutter" là **sai** — docs chính thức chỉ **JSON (DTCG)**.
   (Có vẻ là claim do AI bịa lan trên blog — cảnh giác.)
3. **AI *tạo* design Penpot đẹp còn sớm/experimental** — tạo shape được, nhưng dựa API nội bộ không cam kết.
   Tốt cho prototype, rủi ro nếu làm phụ thuộc cứng.
4. Không có generator ảnh→SwiftUI OSS chín.
5. Không OSS nào tự map design ↔ **component SwiftUI có sẵn của bạn** cho Penpot (Figma có Code Connect,
   Penpot không) → tái tạo bằng ngữ cảnh prompt/skill (DESIGN.md).
6. Nhiều repo "AI design agent" khoe ★ khủng là **hype/không kiểm chứng** — thử trước khi tin.

## Pipeline khuyến nghị (một dòng)

> Penpot (MCP đọc/tạo) → tokens (penpot-export) → Claude Code + skill design-system (DESIGN.md, mô tả
> component library + luật "dùng component, không stack thô") → SwiftUI map component team → SwiftDraw
> cho asset → swift-snapshot-testing so ảnh → **người duyệt baseline**.

Điểm mấu chốt: phần "AI ra SwiftUI" **không có sản phẩm turnkey** cho ràng buộc này — lớp prompt/skill +
snapshot-approval *chính là* sản phẩm bạn phải tự dựng.

## Nguồn (chọn lọc; đầy đủ credibility trong bản gốc)
- Penpot chính thức: github.com/penpot/penpot (/mcp), /penpot-export; help.penpot.app/plugins/api,
  /user-guide/design-tokens (xác nhận token **JSON-only**)
- Figma: github.com/figma/code-connect (MIT, SwiftUI SDK); github.com/GLips/Figma-Context-MCP (MIT)
- SwiftUI gen: github.com/bernaferrari/FigmaToCode (GPL-3.0)
- iOS: github.com/swhitty/SwiftDraw; github.com/bring-shrubbery/SVG-to-SwiftUI;
  github.com/pointfreeco/swift-snapshot-testing
- Kỹ thuật: github.com/voltagent/awesome-design-md; github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Đóng nguồn (cảnh báo): Anima, Locofy, DhiWise/Rocket.new, v0, Google Stitch, Uizard
- Bỏ hoang: tldraw/make-real, exyte/Macaw, mitolog/figma-to-swiftui
