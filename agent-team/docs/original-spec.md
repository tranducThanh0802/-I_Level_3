# Yêu cầu gốc — Agent team (bản lưu, KHÔNG sửa)

> **BÍ DANH: "đề bài".** Khi chủ dự án nói "đề bài", nghĩa là file này (toàn bộ yêu cầu
> Agent team bên dưới). Đây là nguồn chân lý bất biến.
>
> Đây là bản gốc do chủ dự án bàn giao. Giữ nguyên văn để mai sau còn đối chiếu khi
> có tranh cãi về "ý ban đầu là gì". Mọi diễn giải/quyết định phái sinh ghi ở
> DECISIONS.md và PROJECT-CONTEXT.md, KHÔNG sửa vào đây.

---

# Agent team — yêu cầu và đánh giá

Dựng bằng gì, dựng thế nào là việc của mỗi người. File này chỉ chốt ba chuyện: cần những con nào, chúng chạy theo luồng nào, và cuối cùng lấy gì ra đánh giá.

Quy trình không đổi. PO vẫn là người, và spec đã bàn giao chính là đầu vào của agent team.

---

# 1. Bốn con

### Soát spec
Nhận spec cùng docs BE, trả về danh sách chỗ thiếu, chỗ hai bên hiểu khác nhau, kèm bộ câu hỏi soạn sẵn để gửi PO.

Nó cần đối chiếu được spec với docs BE và chỉ đúng chỗ lệch. Cần soi xem spec đã có tiêu chí nghiệm thu kiểm được đúng sai chưa, đã nói đủ bốn trạng thái loading, rỗng, lỗi, mất mạng chưa, dùng API nào, và cái gì lần này không làm. Câu hỏi thì chia hai loại: loại chặn thì dừng đúng phần đó lại chờ, loại đoán được thì cứ chạy tiếp nhưng ghi giả định vào PR cho người review thấy.

Thiếu tiêu chí nghiệm thu, hoặc thiếu tới ba trong bốn trạng thái, thì trả lại spec. Ghi nhận xét rồi vẫn chạy là kiểu tệ nhất — nó sẽ tự bịa phần thiếu và càng làm càng lệch.

### Dev
Nhận spec đã duyệt, trả về PR kèm mô tả, video và ảnh chụp.

Chia task phải có thứ tự và nói rõ task nào chờ task nào. Code theo chuẩn của team, và tự soát lại theo chuẩn trước khi báo xong chứ không đẩy nguyên bản đầu tiên sang cho người đọc.

Có một nhóm việc nó không được tự quyết: tiền, đăng nhập, dữ liệu người dùng, quyền truy cập, xoá dữ liệu, đổi cấu trúc dữ liệu lưu trên máy, đổi API contract, thêm hay đổi thư viện, đổi kiến trúc, sửa cấu hình hoặc khoá hoặc script phát hành, và sửa file ngoài phạm vi task. Gặp mấy chỗ đó thì dừng hỏi.

### Fix bug
Nguồn việc là crash từ store, bug tester báo, user report, hoặc build đỏ. Trả về PR có kèm test chống tái phát.

Việc đầu tiên là gộp trùng — cùng một dấu hiệu lỗi thì cộng đếm, đừng mở bản ghi mới. Sau đó gán mức nặng nhẹ và viết lại các bước tái hiện cho ra hình ra dạng. Trước khi sửa thì tra bug cũ; đã gặp rồi thì lấy lại cách sửa cũ thay vì mò lại từ đầu.

Yêu cầu khó nhất ở con này là **chỉ ra nguyên nhân, không chữa triệu chứng cho test xanh**. Kèm theo đó là một test để bug không quay lại.

Nó dừng hỏi khi bug nằm ở phía BE — lúc đó đóng gói bằng chứng gửi sang, không tự sửa — hoặc khi phải đổi kiến trúc mới hết, hoặc khi thử ba lần vẫn không tái hiện được.

### Test
Nhận tiêu chí nghiệm thu trong spec, trả về kịch bản test, test chạy được, và video luồng vừa sửa.

Kịch bản phải phủ đủ bốn trạng thái. Kết quả chạy phải là kết quả thật, không phải nó tự thuật lại. Nếu tiêu chí nghiệm thu không kiểm được bằng máy thì nó báo lên, đừng tự nghĩ ra tiêu chí thay PO.

---

# 2. Hai luồng

### Luồng feature
```
PO bàn giao spec
      │
      ▼
Soát spec ──► thiếu quá thì trả lại PO
      │
      ├─ câu hỏi chặn ──► gửi PO, mình bấm gửi ──► chờ
      └─ câu hỏi đoán được ──► ghi giả định, chạy tiếp
      │
      ▼
Dev — chia task, làm, tự soát        [build · lint · test]
      │
      ▼
Test — kịch bản, chạy, quay video    [xanh mới đi tiếp]
      │
      ▼
Mở PR: code + video + ảnh
      │
      ▼
Mình duyệt và merge                  ← không nới quyền
      │
      ▼
Build ──► đỏ thì sang luồng fix bug
```

### Luồng fix bug
```
Crash từ store · bug tester · user report · build đỏ
      │
      ▼
Gộp trùng, gán mức, viết lại bước tái hiện
      │
      ▼
Tra bug cũ ──► đã gặp rồi thì lấy cách sửa cũ
      │
      ▼
Tìm nguyên nhân
      │
      ├─ do phía BE ──► gửi bằng chứng sang, bỏ khỏi hàng đợi
      ├─ cần đổi kiến trúc ──► dừng, hỏi
      │
      ▼
Sửa + test chống tái phát            [test cũ và mới đều xanh]
      │
      ▼
Mở PR: code + video + ảnh
      │
      ▼
Mình duyệt và merge
      │
      ▼
Ghi vào bug cũ: nguyên nhân, cách sửa, được hay không
```

Nên làm luồng fix bug trước. Nó có nguồn việc tự đổ vào từ store và CI, tiêu chí xong thì rõ ràng, và quan trọng nhất là không bị chặn bởi chất lượng spec hay bởi lúc PO rảnh.

---

# 3. Bộ nhớ

Chia làm năm chỗ, tách riêng nhau, vì mỗi chỗ được đọc vào lúc khác nhau:

| Chỗ | Chứa gì | Nạp khi nào |
|---|---|---|
| Luật lõi | Không được làm gì, sửa được file nào, chỗ nào phải hỏi | Luôn |
| Việc đang làm | Kế hoạch, đang ở bước mấy, xong gì còn gì | Luôn |
| Cẩm nang | Việc này mấy bước, ví dụ đúng ví dụ sai | Theo loại việc |
| Tri thức dự án | Cấu trúc, chuẩn code, quyết định cũ và lý do | Theo file đang sửa |
| Bug cũ | Đã gặp gì, nguyên nhân, cách sửa, chỗ từng phải sửa tay | Khi gặp bug giống |

Hai chỗ trên cùng luôn được nạp nên phải ngắn, dưới hai trang; dài hơn là chúng đẩy thứ khác ra ngoài. Ba chỗ dưới thì ngược lại, không được nạp hết mọi lúc — cẩm nang gọi theo loại việc đang chạy, tri thức dự án gọi theo file đang chạm tới.

Tất cả nằm trong repo và người khác mở ra đọc được, không nằm trong tài khoản riêng của ai.

Một luật thì chỉ nằm ở một chỗ. Để nó xuất hiện ở hai nơi thì sớm muộn hai nơi lệch nhau, và agent sẽ chọn cái sai.

Agent chỉ được ghi vào hai chỗ: việc đang làm, và bug cũ. Cẩm nang với tri thức dự án do người sửa. Cho nó tự sửa cẩm nang của chính nó thì hai tuần sau không ai biết luật nào còn hiệu lực.

Riêng phần bug cũ có ba đòi hỏi thêm. Phải có khoá để nhận ra trùng, gặp lại thì cộng đếm — chính bộ đếm này về sau cho biết lỗi nào đã lặp ba lần. Mỗi bản ghi phải gắn nhãn được hay không được, kể cả những cách sửa đã thử mà thất bại; thiếu nhãn thì lần sau nó tra ra rồi lặp lại đúng cái sai cũ, mà nhìn từ ngoài lại tưởng hệ thống đang học. Và phải dọn định kỳ, gỡ mấy bug gắn với code đã xoá hay chuẩn đã đổi.

Muốn biết bộ nhớ có thật sự dùng được hay chỉ để cho có, báo lại một bug đã từng sửa và xem nó có tra ra được cách sửa cũ không.

---

# 4. Loop

Một vòng hợp lệ gồm bốn thứ: tiêu chí xong đo được, một bước hành động, một lần máy kiểm, và điều kiện thoát. Thiếu bất kỳ cái nào thì đó không phải loop, chỉ là chạy lại.

Phần máy kiểm là chỗ hầu hết mọi người làm hỏng — nó báo xong và vòng lặp tin. Kiểm phải là thứ chạy được và trả về đúng sai: build, test, lint, so ảnh chụp, hoặc một con khác đọc lại theo checklist. Nó tự khen thì không tính.

Ba cái chặn để nó không chạy vô hạn: thử cùng một bước quá ba lần thì dừng, hết ngân sách thời gian thì dừng, và hai vòng liền ra kết quả y hệt thì cũng dừng vì lúc đó nó đang xoay tại chỗ. Giao thử một việc không thể xong là biết ngay có chặn hay không.

Trạng thái phải nằm ngoài context: kế hoạch, bước đang làm, việc đã xong, việc còn lại đều ghi ra file. Tắt giữa lúc đang chạy rồi mở lại, nó phải tiếp từ chỗ đứt.

Cần đủ ba tầng, không phải một:

| Loop | Một vòng là gì | Thoát khi nào |
|---|---|---|
| Trong | Một bước code → build, test | Test xanh, hoặc quá ba lần thì dừng |
| Giữa | Một task → tự soát → mở PR | Đủ tiêu chí nghiệm thu của task |
| Ngoài | Gom chỗ sửa tay → sửa cẩm nang | Chạy định kỳ, không có điểm thoát |

Hai tầng đầu chỉ giúp làm xong việc. Tầng ngoài mới là thứ khiến tháng sau khác tháng này, nên đa số người dừng ở hai tầng đầu rồi thắc mắc sao mấy tháng vẫn phải sửa tay đúng mấy lỗi cũ.

Tầng ngoài có ba đòi hỏi riêng: chỉ sửa cẩm nang khi một lỗi đã lặp từ ba lần, vì một lần là ngoại lệ và nhét ngoại lệ vào cẩm nang thì nó phình lên rồi tự mâu thuẫn; giữ một bộ hai mươi tình huống lấy từ việc thật để chạy lại mỗi lần cẩm nang hay chuẩn thay đổi, thấy tệ đi thì chặn; và mọi thay đổi cẩm nang đều qua người duyệt. Thử sửa hỏng một dòng trong cẩm nang, bộ hai mươi tình huống phải bắt được.

---

# 5. Áp cho cả bốn con

Tiêu chí xong luôn phải là thứ máy trả lời đúng sai được. "Làm cho đẹp" thì nó không biết đường nào mà đi.

Merge và đẩy lên store thì chưa nới quyền, kể cả khi mọi thứ đã chạy êm vài tháng.

Câu hỏi nó gửi cho mình phải đọc xong trả lời được trong ba mươi giây: chỗ vướng, hai cách kèm hệ quả, nó nghiêng về cách nào và vì sao, cùng với việc nó sẽ làm gì nếu quá hạn không ai trả lời. Kiểu "chỗ này em không rõ, anh xem giúp" thì không nhận. Và trong lúc chờ, nó vẫn phải chạy tiếp được mấy phần không liên quan.

Bàn giao gồm ba thứ: code, video quay màn hình luồng vừa sửa, ảnh chụp trước và sau. Thiếu video thì chưa xong, vì nhìn diff không đoán được UI đúng hay sai, mà tự build lên máy chạy thử thì mất đúng khoản thời gian đang cố cắt.

Mỗi lần mình phải sửa tay output của nó thì ghi một dòng — đây là đầu vào của loop ngoài:
```
Loại: sai chuẩn / thiếu thông tin đầu vào / hiểu sai yêu cầu / sai logic
Cụ thể: <một câu>
```

Mọi lần chạy đều tra lại được: việc gì, mấy giờ, đi qua bước nào, hỏng ở đâu, người sửa tay bao nhiêu, cuối cùng dùng được hay bỏ. Bốc ngẫu nhiên một việc tuần trước, phải mở ra xem lại được.

Và cuối cùng, người khác bấm thử phải chạy được. Chỉ mình bạn chạy được thì đó là mẹo cá nhân, chưa phải hệ thống.

Về docs BE thì tuỳ cấu hình team. Nếu BE là team khác, agent đọc bản chính và phải phát hiện được khi bản đó đổi, tuyệt đối không tự sửa gì phía BE. Nếu BE cùng team thì đừng cho nó tự đổi API contract để làm khớp — cách nhanh nhất để test xanh là đổi field ở BE, mà làm vậy là vừa phá contract; thêm nữa, đổi API thì bản app cũ đang nằm trên máy người dùng vẫn phải chạy được.

---

# 6. Đánh giá

Tính từ lúc nhận spec đến lúc merge. Phần PO viết spec không tính, vì đó không phải phần mình cắt.

Khoản chờ PO trả lời thì đo nhưng để riêng. Agent cắt được phần ngồi đọc spec đối chiếu docs BE, thường một tới ba tiếng mỗi task; còn thời gian chờ thì nó không cắt được gì, có khi còn dài hơn cả phần đọc. Gộp hai khoản vào một là ra số xấu vì lý do không phải lỗi hệ thống.

Mấy số cần theo:

| Số | Ghi chú |
|---|---|
| Thời gian người bỏ ra, theo từng loại việc | So cùng loại, độ khó tương đương |
| Thời gian chờ ngoài | Để riêng |
| Tỷ lệ dùng được ngay, không phải sửa | |
| Số lần sửa tay, kèm ba loại hay gặp nhất | Cho biết đang yếu chỗ nào |
| Số việc bỏ giữa chừng, quay về làm tay | Bắt buộc có |
| Bug gộp trùng được bao nhiêu | Luồng fix bug |
| Bug quay lại sau khi đã sửa | Luồng fix bug — cao là đang chữa triệu chứng |
| Số câu hỏi agent gửi mỗi tuần | Nhiều là luật chưa rõ, ít mà vẫn có sự cố là nó tự quyết bừa |

Khi so thì lấy cùng loại việc, độ khó tương đương, mỗi loại tối thiểu năm mẫu mỗi bên. Dùng con số nằm giữa chứ đừng dùng trung bình, vì một việc dài bất thường sẽ kéo lệch cả bảng, và nó luôn kéo về hướng có lợi cho người báo cáo.

Có ba thứ không tính: việc không có ghi lại thì không được đưa vào phần đã cắt; tỷ lệ thành công tròn trăm phần trăm nghĩa là đang giấu việc bỏ dở; và "thấy nhanh hơn" mà không kèm số thì cũng vậy.

Để biết đang ở đâu:

| Bậc | Có gì |
|---|---|
| 1 | Một con làm được một bước, gọi tay từng lần |
| 2 | Một con chạy liền cả luồng của nó, mình chỉ duyệt đầu và cuối |
| 3 | Cả hai luồng chạy được, tự nhận việc từ store và CI |
| 4 | Nhiều con, có con điều phối, tự tìm việc |

Đạt là: bậc 2 trở lên, thời gian mình bỏ ra ở nhóm việc lặp lại giảm ít nhất bốn mươi phần trăm, việc bỏ giữa chừng dưới hai mươi phần trăm, bug quay lại dưới mười phần trăm, số liệu tra lại được tới từng việc, và người khác bấm thử chạy được.

Chưa đạt là: không có số, hoặc có số mà không lần về được từng việc, hoặc chỉ mình bạn chạy được.

---

# Biết trước cho khỏi đánh giá lệch

Không phải việc gì cũng chạy êm như nhau, nên đừng lấy số ở loại này áp cho loại kia.

Chạy êm nhất là sửa bug có stack trace, refactor có test bao phủ, viết test từ tiêu chí, soát spec, và mấy đoạn code lặp lại.

Nhóm thứ hai chạy được nhưng vẫn cần người xem: mọi thứ mà đúng hay sai phải nhìn mới biết — animation, khoảng cách, cảm giác. Đây đúng là lý do bàn giao phải có video.

Nhóm hay đứng là việc dài nhiều giờ cần quyết định kiến trúc giữa đường, race condition, và vấn đề hiệu năng. Nguy nhất trong nhóm này là spec mơ hồ, vì nó sẽ tự bịa giả định rồi chạy tiếp, mà giả định sai thì càng chạy càng xa.

Đừng lấy nhóm cuối làm phép thử đầu tiên rồi kết luận công nghệ chưa tới.
