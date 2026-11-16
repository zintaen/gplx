# Đánh giá mức độ dễ dùng (mô phỏng) – Ôn lý thuyết lái xe

Ngày đánh giá: 17/11/2026 · Phiên bản đánh giá: commit `38225e2` (nhánh `main`)

**Trạng thái:** V1–V15 đã được triển khai theo các khuyến nghị ở mục 5 (17/11/2026). Kế hoạch kiểm chứng ở mục 7 vẫn chưa làm với người dùng thật.

> **Đây là đánh giá mô phỏng, không phải nghiên cứu với người dùng thật.** Mỗi nhận định được gắn nhãn:
> **[QS]** quan sát trực tiếp trên sản phẩm hoặc mã nguồn · **[GT]** suy luận, giả thuyết cần kiểm chứng · **[GL]** hành vi hoặc lời nói giả lập của persona.
> Không có số liệu thời gian, tỷ lệ thành công hay phản hồi thật nào trong tài liệu này.

---

## 1. Sản phẩm, phạm vi và giới hạn

**Sản phẩm.** Trang web tĩnh, một tệp `index.html`, giúp người học ôn sát hạch lý thuyết cho 15 hạng giấy phép lái xe từ bộ 600 câu của Cục CSGT (2025) và 120 tình huống mô phỏng (Thông tư 17/2026/TT-BXD). Không cần tài khoản; tiến độ lưu trong `localStorage` của trình duyệt.

**Giá trị cốt lõi:** biết phải học gì trước (lộ trình theo rủi ro: điểm liệt → câu dễ nhầm → nhóm còn lại), luyện đúng cấu trúc đề của hạng mình, và biết mình đã sẵn sàng thi chưa.

**Hành trình chính**

1. Lần đầu vào: chọn hạng → Lộ trình.
2. Học theo nhóm: trả lời → nhận phản hồi → câu tiếp.
3. Thi thử: đề có giờ → nộp → xem lại → ôn câu sai.
4. Tra cứu: Sổ tay con số, Câu sai.
5. Mô phỏng (chỉ hạng ô tô): học theo nhóm, nhận diện tên, kiểm tra thử 10 tình huống.
6. Quay lại lần sau: “Tiếp tục ôn hạng X” → “Học tiếp”.

**Đã kiểm tra trực tiếp** trên bản chạy ở máy (`localhost:8765`), khung 375×812 (điện thoại), chế độ tối, với dữ liệu trắng:

- Trang chọn hạng; chọn B, sau đó đổi sang A1.
- Lộ trình hạng B và A1; nút “Học tiếp”.
- Học nhóm điểm liệt: trả lời sai, đúng, bằng phím số; nút Câu trước/Câu tiếp; thoát rồi vào lại.
- Thi thử hạng B: chọn đáp án, thoát giữa chừng (huỷ), nộp sớm khi còn 29 câu trống, màn kết quả.
- Câu sai, Sổ tay (hạng B và A1).
- Mô phỏng: trang chính, nhóm “Xử lý riêng”.
- Đo kích thước vùng chạm, tràn ngang, thuộc tính trợ năng bằng JavaScript.

Hộp thoại `confirm` được thay bằng hàm ghi lại nội dung để đi tiếp. Sau khi kiểm tra đã xoá `localStorage` của trang thử.

**Chưa kiểm tra (không kết luận tốt hay xấu)**

- Điện thoại thật, iOS Safari, Android cũ, màn hình 320 px.
- Trình đọc màn hình thật (VoiceOver, TalkBack). Chỉ đọc mã và thuộc tính ARIA.
- Hết giờ tự nộp bài; tải lại trang giữa bài thi; đồng bộ giữa nhiều tab.
- Mở liên kết PDF gốc trên điện thoại; phát video YouTube.
- Chế độ sáng (chỉ chụp chế độ tối); phóng chữ hệ thống 200%.
- Kiểm tra thử mô phỏng và Nhận diện tên chạy hết vòng (chỉ đọc mã).
- Mạng chậm hoặc ngắt mạng.

---

## 2. Persona

Mỗi persona khác nhau ở mục tiêu, kinh nghiệm và hạn chế cụ thể; hạn chế được ghi rõ, không suy ra từ tuổi hay nghề.

| # | Persona | Hạng | Bối cảnh, thiết bị | Kinh nghiệm công nghệ / lĩnh vực | Mục tiêu và hạn chế cụ thể |
|---|---|---|---|---|---|
| P01 | Lan, 19, sinh viên | A1 | Android tầm trung, 4G yếu ở ký túc xá | Thành thạo app / chưa biết luật | Học 10 phút giữa giờ; lần đầu vào |
| P02 | Hùng, 34, tài xế xe ôm công nghệ | B | Điện thoại, học lúc chờ khách | Dùng app hằng ngày / biết luật xe máy | Quen gọi “bằng B2”; hay bị cắt ngang |
| P03 | Cô Mai, 52, nội trợ | B | Điện thoại, học buổi tối | Chủ yếu dùng Zalo, Facebook / mới | Muốn “bằng B1 số tự động” theo cách gọi cũ; đặt cỡ chữ hệ thống lớn |
| P04 | Tuấn, 27, kỹ sư phần mềm | B | Laptop, bàn phím | Rất thành thạo / mới | Muốn học nhanh bằng phím, tối ưu theo số liệu |
| P05 | Ông Tư, 66, nghỉ hưu | A1 | Điện thoại của con | Ít dùng web / biết đi xe đạp | Muốn chạy xe máy điện; không chắc xe mình bao nhiêu kW |
| P06 | Ngọc, 30, nhân viên văn phòng | B | iPhone, dùng VoiceOver | Thành thạo trình đọc màn hình / mới | Không nhìn được hình sa hình; cần nhãn rõ |
| P07 | Phát, 18, học sinh lớp 12 | A1 | Điện thoại | Thành thạo / mới | Ôn dồn 2 ngày trước khi thi |
| P08 | Cô Hà, 41, giáo viên trung tâm đào tạo | B, C | Laptop, máy chiếu | Trung bình / chuyên môn cao | Cần mở nhanh “câu 145” để giảng; kiểm tra Sổ tay |
| P09 | Minh, 45, tài xế xe tải nâng hạng | C | Điện thoại màn hình lớn | Trung bình / nhiều năm lái | Quen phần mềm 600 câu của trung tâm |
| P10 | Khoa, 29, lái xe khách nâng hạng | D | Điện thoại | Thành thạo / có kinh nghiệm | Đề 45 câu, 26 phút; ít thời gian |
| P11 | Thảo, 36, mẹ hai con nhỏ | B | Điện thoại, hay khoá máy giữa chừng | Thành thạo / mới | Học từng 5 phút, thường phải bỏ dở |
| P12 | Duy, 22, sinh viên | B | Điện thoại | Thành thạo / mới | Dễ mất tập trung với trang dài; cần phiên ngắn, phản hồi rõ |
| P13 | Kim, 31, người Hàn sống ở VN | B | Điện thoại | Thành thạo / có bằng nước ngoài | Đọc tiếng Việt chậm; cần câu chữ ngắn, nhất quán |
| P14 | Bảo, 25, từng trượt lý thuyết | B | Điện thoại | Thành thạo / đã học hết | Trượt vì sai câu điểm liệt; muốn tập trung chỗ yếu |
| P15 | Trang, 33, kế toán | B | iPad, chế độ tối, buổi tối | Thành thạo / mới | Học đều mỗi tối 30 phút |
| P16 | Long, 38, nhân viên ngân hàng | B | Máy tính cơ quan, mạng chặn YouTube | Trung bình / mới | Học giờ nghỉ trưa |
| P17 | Hiếu, 40, buôn bán | B1 | Điện thoại | Ít / biết đi xe máy | Cần bằng lái xe ba bánh chở hàng |
| P18 | Quân, 50, tài xế đầu kéo | CE | Điện thoại | Ít / rất nhiều kinh nghiệm lái | Thích làm đề liên tục, ít đọc hướng dẫn |
| P19 | Nhi, 24, nhân viên bán hàng | B | Điện thoại | Thành thạo / đã thuộc gần hết | Chỉ còn thi thử dồn dập trước ngày thi |
| P20 | Sơn, 31, công nhân | A | Android cũ, màn hình nhỏ, gói data ít | Trung bình / biết luật cơ bản | Tiết kiệm dữ liệu |
| P21 | Linh, 28, nhân viên marketing | B | Điện thoại | Thành thạo / mới | Trung tâm yêu cầu qua bài kiểm tra mô phỏng |
| P22 | Phong, 47, kỹ thuật viên | B | Điện thoại để cỡ chữ lớn nhất | Trung bình / mới | Ngón tay to, hay chạm nhầm nút nhỏ |
| P23 | Yến, 35, dùng chung điện thoại với chồng | A1 (Yến), B (chồng) | Một điện thoại, một trình duyệt | Trung bình / mới | Hai người cùng ôn trên một máy |
| P24 | Đạt, 20, sinh viên | B | Điện thoại + laptop | Thành thạo / mới | Học trên cả hai thiết bị, mong tiến độ đi theo |

---

## 3. Tác vụ và kết quả mô phỏng

**Tác vụ**

- **T1** Lần đầu vào: hiểu trang dùng để làm gì, chọn đúng hạng.
- **T2** Học nhóm đầu tiên (điểm liệt), hiểu vì sao mình sai.
- **T3** Làm một đề thi thử, đọc kết quả, ôn lại câu sai.
- **T4** Tra cứu: mở một câu theo số, tìm con số trong Sổ tay.
- **T5** Phục hồi sau thao tác sai: chạm nhầm đáp án, thoát giữa chừng, nộp sớm.
- **T6** Quay lại lần sau, học tiếp đúng chỗ.
- **T7** Học và kiểm tra thử mô phỏng (hạng ô tô).

**Ký hiệu kết quả dự kiến:** ✅ dễ hoàn thành · 🔍 cần dò tìm · 🆘 cần trợ giúp · ❌ không hoàn thành. Ô trống: persona không làm tác vụ đó.

| Persona | T1 | T2 | T3 | T4 | T5 | T6 | T7 |
|---|---|---|---|---|---|---|---|
| P01 Lan (A1) | ✅ | ✅ | | | | ✅ | |
| P02 Hùng (B) | 🔍 | | ✅ | | 🔍 | 🔍 | |
| P03 Mai (B) | ❌ | 🆘 | | | | | |
| P04 Tuấn (B) | ✅ | ✅ | ✅ | 🔍 | 🔍 | | |
| P05 Ông Tư (A1) | 🆘 | | | | | | |
| P06 Ngọc (B, VoiceOver) | | 🔍 | 🆘 | | | | |
| P07 Phát (A1) | ✅ | 🔍 | ✅ | | | | |
| P08 Hà (giáo viên) | | | | ❌ | | | |
| P09 Minh (C) | ✅ | | 🔍 | | | | |
| P10 Khoa (D) | | | 🔍 | | | | |
| P11 Thảo (B) | | | 🔍 | | ❌ | 🔍 | |
| P12 Duy (B) | | 🔍 | | | | 🔍 | 🔍 |
| P13 Kim (B) | 🔍 | 🆘 | | 🔍 | | | |
| P14 Bảo (B) | | | ✅ | | | 🔍 | |
| P15 Trang (B, iPad) | | ✅ | | ✅ | | ✅ | |
| P16 Long (B) | | | | | | | 🔍 |
| P17 Hiếu (B1) | ✅ | | | | | | |
| P18 Quân (CE) | | | 🔍 | | 🔍 | | |
| P19 Nhi (B) | | | ✅ | | 🔍 | | |
| P20 Sơn (A) | | | | 🔍 | | | |
| P21 Linh (B) | | | | | | | 🆘 |
| P22 Phong (B) | | | 🔍 | | 🔍 | | |
| P23 Yến (A1+B) | | | | | | 🔍 | |
| P24 Đạt (B) | | | | | | ❌ | |

### Chi tiết các lượt đáng chú ý

**P03 Mai – T1 Chọn hạng (❌)**
- Mục tiêu: học “bằng B1 số tự động” như trung tâm gọi.
- Luồng: thấy mục “Mô tô” có ô **B1** → chạm vào vì trùng tên.
- [QS] Thẻ B1 ghi “Mô tô ba bánh, và xe hạng A1”; không thẻ nào nhắc tên hạng cũ (tìm “B2”, “số tự động”, “A2” trong mã và dữ liệu: không có).
- [GT] Người đọc lướt chỉ nhìn mã hạng sẽ học nhầm bộ 300 câu mô tô; có thể chỉ phát hiện khi đề thi thử chỉ có 25 câu.
- [GL] “Trung tâm bảo chị thi B1 mà, sao ở đây B1 lại là xe ba bánh?”

**P02 Hùng – T1 (🔍):** [GL] “B2 đâu nhỉ… à chắc là B, ô tô đến 8 chỗ.” Tìm được nhờ đọc mô tả, nhưng phải đoán.

**P05 Ông Tư – T1 (🆘):** [QS] A1 là “đến 125 cm³ hoặc động cơ điện đến 11 kW”, A là “trên 11 kW”. [GL] “Xe điện của tôi bao nhiêu kW thì tôi chịu, phải hỏi cháu.” [GT] Đa số xe máy điện phổ thông thuộc A1, nhưng trang không nói cách kiểm tra.

**P03 Mai, P13 Kim – T2 học điểm liệt (🆘)**
- [QS] Khi sai, phản hồi là “Chưa đúng. Đáp án là ý 2.”, kèm ghi chú câu bẫy, câu song sinh và liên kết “Xem câu 19 trong tài liệu gốc, trang 7 của PDF”.
- [QS] PDF gốc nặng khoảng 6 MB và chỉ gạch chân đáp án, không giải thích.
- [GL] Kim: “Tôi biết đáp án là 2 rồi, nhưng tại sao? Mở PDF thì cũng chỉ thấy gạch chân.”
- [GT] Người chưa có kiến thức nền sẽ học thuộc vị trí đáp án thay vì hiểu, trái với thông điệp “Vì sao không học mẹo” của chính trang.

**P04 Tuấn – T2 (✅):** [QS] Phím 1–3 chọn đáp án, Enter/→ sang câu, focus nằm ở câu hỏi mới. [GL] “Nhanh, không cần chuột.”

**P12 Duy – T2/T6 (🔍)**
- [QS] Sau khi sai 1 câu điểm liệt rồi quay về Lộ trình, nút chính đổi từ “Học tiếp · Rượu bia, ma túy…” thành “Ưu tiên · Ôn lại 1 câu đang sai”.
- [GL] “Ơ, mình đang học nhóm rượu bia mà, giờ nút lại bắt ôn 1 câu?”
- [GT] Mỗi lần sai một câu điểm liệt, mạch học bị cắt; muốn học tiếp nhóm phải cuộn xuống phần “Các chặng”.

**P11 Thảo – T5 nộp sớm (❌)**
- Bối cảnh: đang làm đề thì con khóc, bấm “Nộp bài” để xem nhanh mình đúng mấy câu.
- [QS] Hộp thoại “Còn 29 câu chưa làm. Nộp bài luôn?” → đồng ý. Kết quả: 29 câu chưa từng mở bị ghi là “câu sai”. Câu sai tăng lên 31; nút chính ở Lộ trình thành “Ôn lại 31 câu đang sai”.
- [QS] Theo mã (`finish()` gọi `mark(x, false)` cho câu bỏ trống), câu đã thuộc nếu bị bỏ trống cũng mất trạng thái “đã thuộc”.
- [GL] “Mình mới làm có 1 câu mà giờ báo sai 31 câu? Danh sách câu sai giờ vô nghĩa.”
- Không có cách hoàn tác, ngoài “Xóa tiến độ” (xoá toàn bộ).

**P22 Phong, P18 Quân – T3/T5 thi thử (🔍)**
- [QS] Chạm một đáp án là bài tự chuyển ngay sang câu sau; ô số trên lưới chuyển màu xanh.
- [QS] Ô lưới 30×30 px, 10 cột ở bề ngang 375 px.
- [QS] Nút quay lại ‹ ở đầu trang chỉ 17×30 px. Đây là lối thoát duy nhất trong màn học và thi (thanh tab bị ẩn).
- [GL] Phong: “Tôi bấm nhầm ý 1 mà nó nhảy qua câu khác rồi, quay lại thì phải bấm ô số tí xíu.”
- [GT] Người không để ý ô số đổi màu sẽ không biết câu trước đã lưu đáp án nào.

**P09 Minh, P10 Khoa – T3 (🔍)**
- [QS] Màn thi hiện cùng lúc “Câu 2 trong đề” và “Câu 11” (số câu trong bộ 600).
- [GL] Minh: “Đây là câu 2 hay câu 11? Phần mềm trung tâm chỉ có một số thôi.”

**P06 Ngọc – T3 VoiceOver (🆘, chỉ đánh giá từ mã)**
- [QS] Đồng hồ `#timer` không có `aria-live`; không có cảnh báo sắp hết giờ (cả bằng hình lẫn bằng lời).
- [QS] Hình sa hình có alt chung “Hình minh họa câu N”, không mô tả nội dung.
- [QS] Ô lưới có `aria-label` đầy đủ (“Câu 4, chưa trả lời, điểm liệt”). Đáp án có `aria-pressed`. Đây là điểm tốt.
- [GT] Câu sa hình và biển báo gần như không làm được bằng trình đọc màn hình. Đây là giới hạn nội dung, khó sửa triệt để.

**P08 Cô Hà – T4 mở câu 145 (❌)**
- [QS] Sổ tay ghi “Số câu nằm ở cột bên phải để bạn mở lại”, nhưng các số câu là chữ thường, không bấm được.
- [QS] Không có ô tìm hay đường dẫn để mở một câu theo số. Bảng “Sai nhiều lần nhất” ở tab Câu sai cũng không bấm được.
- [GL] “Học viên hỏi câu 145, tôi không mở được câu đó ở đây.”

**P20 Sơn, P13 Kim – T4 Sổ tay trên màn hình nhỏ (🔍)**
- [QS] Ở 375 px, cả 6 bảng của Sổ tay đều tràn ngang (`min-width: 480px`).
- [QS] Cột “Câu”, cột mà đoạn giới thiệu nhắc tới, nằm ngoài màn hình; phải vuốt ngang mới thấy.

**P21 Linh – T7 Mô phỏng (🆘)**
- [QS] Vào “Xử lý riêng từng tình huống”, tình huống 1 hiện ngay 3 câu trắc nghiệm, mỗi câu 4 lựa chọn (dấu hiệu gián tiếp, trực tiếp, xử lý). Đáp án đầy đủ chỉ hiện sau khi trả lời đủ 3 ý.
- [GL] “Mình chưa học gì cả mà đã bắt chọn. Lần đầu toàn đoán.”
- [QS] “Nhận diện tên tình huống” chạy 120 câu liền, đếm đúng/sai chỉ trong phiên; thoát là mất. Ô đếm ở trang Mô phỏng luôn ghi “120”.

**P16 Long – T7 (🔍):** [QS] Video tải khi bấm, nguồn YouTube; trang có báo trước nguồn. [GT] Mạng cơ quan chặn YouTube thì khung video lỗi; trang không có thông báo riêng cho trường hợp này (chưa kiểm tra).

**P24 Đạt – T6 (❌):** [QS] Tiến độ chỉ lưu trên trình duyệt; trang có ghi rõ “Tiến độ chỉ lưu trên trình duyệt này”. Học trên laptop thì điện thoại vẫn trống. Trang báo trước nên đây là giới hạn đã công bố, không phải lỗi; ghi lại vì ảnh hưởng tác vụ.

**P23 Yến – T6 (🔍):** [QS] Tiến độ dùng chung giữa các hạng (trang có báo trước). Khi đổi sang A1, các câu sai trong đề B mà thuộc bộ A1 vẫn hiện (thấy “Ôn lại 20 câu đang sai” ở A1). [GT] Hai người dùng chung máy sẽ trộn tiến độ của nhau.

**P01 Lan, P15 Trang – T6 (✅):** [QS] Trang chọn hạng có nút “Tiếp tục · Ôn hạng B · x/600 câu đã thuộc”. Vào nhóm đang học thì mở thẳng ở câu đầu tiên chưa thuộc.

---

## 4. Điểm đang hoạt động tốt (nên giữ)

- **Chọn hạng có đủ thông tin.** [QS] Mỗi thẻ ghi số câu, phút, điểm đạt, cỡ bộ câu.
- **Lộ trình xếp theo rủi ro, có lý do.** [QS] Có bảng “Mỗi đề / Trong bộ / Đã thuộc” và giải thích cách ước tính.
- **Học tiếp đúng chỗ.** [QS] Vào nhóm thì mở ở câu đầu tiên chưa thuộc.
- **Ngăn mất bài thi.** [QS] Bấm ‹ giữa bài thi có hộp xác nhận, huỷ thì ở lại bài. Nút Back của trình duyệt được xử lý cùng đường trong mã (chưa thử trực tiếp). Nộp khi còn câu trống cũng có hộp hỏi lại.
- **Phản hồi giàu ngữ cảnh.** [QS] Ghi chú câu bẫy trích đúng phương án gộp của câu đó; ghi chú câu song sinh có số câu đối chiếu.
- **Bàn phím và focus.** [QS] Phím số và mũi tên dùng được; focus đặt vào câu hỏi mới; ô lưới thi có nhãn ARIA đầy đủ.
- **Trạng thái trống có hướng dẫn.** [QS] Ví dụ: “Chưa có câu sai. Làm một nhóm ở Lộ trình hoặc một đề Thi thử…”.
- **Có chế độ tối; không tràn ngang toàn trang ở 375 px** [QS] (chỉ bảng Sổ tay tràn trong khung cuộn riêng).
- **Video chỉ tải khi bấm, có nói nguồn. Nguồn pháp lý ghi rõ** ở chân trang. [QS]

---

## 5. Danh sách vấn đề (theo mức độ và ảnh hưởng tới tác vụ cốt lõi)

Thang mức độ:

- **Nghiêm trọng:** làm hỏng mục tiêu ôn đúng hạng hoặc làm sai lệch dữ liệu học.
- **Cao:** cản trở tác vụ chính với nhiều nhóm.
- **Trung bình:** gây chần chừ hoặc thao tác thừa.
- **Thấp:** khó chịu nhỏ.

Loại vấn đề: **[Chức năng]** là hành vi có thể coi là lỗi; **[Usability]** là chức năng chạy đúng ý đồ nhưng khó dùng.

### V1. Tên hạng mới không nối với tên hạng cũ người học vẫn dùng · Nghiêm trọng · [Usability]

- **Vị trí:** trang chọn hạng (`chooser()`, `index.html:345`).
- **Bằng chứng [QS]:**
  - Thẻ chỉ có mã hạng mới và mô tả kỹ thuật.
  - Không có chữ “B2”, “số tự động”, “A2” trong mã nguồn và dữ liệu.
  - Mã “B1” nay là mô tô ba bánh, nằm trong mục Mô tô.
- **Ảnh hưởng [GT]:** người quen tên cũ có thể chọn nhầm B1 và ôn sai bộ câu (300 thay vì 600), sai cấu trúc đề. Phát hiện muộn thì tốn công.
- **Persona:** P03, P02, P05; người được người khác (trung tâm, người thân) dặn theo tên cũ.
- **Nguyên nhân có thể:** trang theo đúng văn bản mới, nhưng ngôn ngữ đời thường vẫn dùng tên theo luật cũ.
- **Giải pháp:** thêm một dòng “Trước đây gọi là …” trên thẻ những hạng bị đổi tên hoặc gộp. Ví dụ:
  - **B** · Ô tô chở người đến 8 chỗ… · *Trước đây: B1 (số tự động), B2*
  - **B1** · Mô tô ba bánh… · *Khác B1 ô tô số tự động trước đây: nếu bạn học lái ô tô, chọn hạng B*
  - **A** · … · *Trước đây: A2*

  Đồng thời thêm một đoạn ngắn dưới tiêu đề: “Từ 01/01/2025 tên hạng đã đổi. Học lái ô tô con (số sàn hoặc số tự động) → chọn **B**.”
  > Cần đối chiếu bảng chuyển đổi tên hạng với Luật TTATGTĐB 2024 và văn bản hướng dẫn trước khi ghi; báo cáo này chưa kiểm chứng toàn bộ bảng chuyển đổi.
- **Trade-off:** thẻ dài thêm một dòng. Phương án khác là hộp hỏi lại khi chọn B1 (“Bạn muốn học xe ba bánh hay ô tô số tự động?”), chặn nhầm tốt hơn nhưng thêm một bước cho người chọn đúng. **Khuyến nghị:** dòng chữ trên thẻ trước; chỉ thêm hộp hỏi lại nếu thử nghiệm vẫn thấy chọn nhầm.
- **Kiểm chứng:** người chỉ được dặn “thi B2” hoặc “B1 số tự động” chọn đúng hạng B ngay lần đầu, không cần hỏi lại.

### V2. Nộp bài sớm biến câu bỏ trống thành “câu sai” và xoá trạng thái đã thuộc · Nghiêm trọng · [Chức năng + Usability]

- **Vị trí:** Thi thử → Nộp bài (`finish()`, `index.html:534`: `mark(x, ok)` cho mọi câu, kể cả câu bỏ trống).
- **Bằng chứng [QS]:** trả lời 1 câu, nộp khi còn 29 câu trống. Kết quả: 31 câu trong Câu sai; CTA Lộ trình thành “Ôn lại 31 câu đang sai”. Hộp xác nhận chỉ hỏi “Còn 29 câu chưa làm. Nộp bài luôn?”, không báo hậu quả.
- **Ảnh hưởng:**
  - Danh sách Câu sai, tỷ lệ đã thuộc và ước tính khả năng đạt bị sai lệch.
  - Câu đã thuộc mà bị bỏ trống mất trạng thái “đã thuộc” [QS từ mã].
  - Không có hoàn tác.
- **Persona:** P11, P19, P02, bất kỳ ai nộp sớm để xem điểm.
- **Giải pháp (khuyến nghị):** câu bỏ trống vẫn tính sai trong điểm của đề, nhưng **không ghi vào tiến độ học**. Tức là `mark()` chỉ chạy cho câu có trả lời.
- **Phương án khác:** ghi câu trống vào tiến độ nhưng đổi chữ trong hộp xác nhận thành “29 câu bỏ trống sẽ tính là sai và được đưa vào Câu sai”. Trade-off: rõ ràng nhưng vẫn làm loãng danh sách. Không khuyến nghị.
- **Kiểm chứng:** nộp đề khi còn N câu trống thì Câu sai chỉ tăng đúng số câu đã trả lời sai; câu đã thuộc vẫn thuộc.

### V3. Phản hồi khi sai không cho biết vì sao · Cao · [Usability / nội dung]

- **Vị trí:** phản hồi trong Học, Xem lại bài thi (`feedback()`, `index.html:420`).
- **Bằng chứng [QS]:** chỉ có “Chưa đúng. Đáp án là ý 2.”, ghi chú bẫy hoặc song sinh, và liên kết tới PDF gốc. PDF nặng khoảng 6 MB, chỉ gạch chân đáp án.
- **Ảnh hưởng [GT]:** người mới học thuộc vị trí đáp án, dễ sai ở câu song sinh. Mở PDF trên điện thoại tốn dữ liệu (P20) mà không có thêm thông tin.
- **Persona:** P03, P13, P07, P12.
- **Giải pháp không cần viết thêm nội dung:** dữ liệu Sổ tay đã có cột “Câu” trỏ tới từng câu. Đảo ngược ánh xạ đó để hiện ngay trong phản hồi dòng quy tắc liên quan. Ví dụ ở câu 145:

  > **Quy tắc liên quan (Sổ tay):** Trong khu đông dân cư, ô tô và xe mô tô trên đường đôi được chạy tối đa 60 km/h.

  Thêm cỡ tệp vào liên kết: “Xem trong tài liệu gốc (PDF, 6 MB)”.
- **Trade-off:** chỉ phủ các câu có trong Sổ tay. Viết giải thích cho cả 600 câu là việc nội dung lớn, cần người có chuyên môn duyệt; chỉ nên làm nếu thử nghiệm cho thấy cần.
- **Kiểm chứng:** với câu có trong Sổ tay, người học giải thích lại được vì sao đáp án đúng; câu song sinh làm đúng ở lần gặp sau.

### V4. Không mở được một câu theo số · Cao · [Usability]

- **Vị trí:**
  - Sổ tay: cột “Câu”, có câu dẫn “để bạn mở lại”.
  - Câu sai: bảng “Sai nhiều lần nhất”.
  - Không có ô tìm kiếm.
- **Bằng chứng [QS]:** không có liên kết hay nút nào trong các bảng (đếm được 0). Lời dẫn hứa một hành động không làm được.
- **Persona:** P08, P04, P13; học viên được thầy giao “xem lại câu 145”.
- **Giải pháp:** biến mỗi số câu thành liên kết `#cau/145`, mở màn học một câu (dùng lại `study()` với danh sách 1 câu). Hàng trong “Sai nhiều lần nhất” cũng bấm được. Nếu chưa làm được, sửa lời dẫn cho khớp thực tế (bỏ “để bạn mở lại”).
- **Trade-off:** thêm một route. Ô tìm theo số hoặc từ khoá là chức năng mới, chưa cần nếu liên kết đã giải quyết được.
- **Kiểm chứng:** từ Sổ tay mở được câu 145 trong một lần chạm; từ Câu sai mở được câu sai nhiều nhất.

### V5. Thi thử: chạm đáp án là chuyển câu ngay · Trung bình · [Usability]

- **Vị trí:** màn thi (`runExam()`, `index.html:523`).
- **Bằng chứng [QS]:** chọn đáp án thì sang câu tiếp ngay, không còn thấy lựa chọn vừa chạm.
- **Ảnh hưởng [GT]:** chạm nhầm không kịp thấy; người dùng phải tìm lại ô số nhỏ để sửa; không chắc đã lưu.
- **Persona:** P22, P18, P03.
- **Phương án:**
  - (a) Giữ ở câu hiện tại, tô đáp án đã chọn, nút “Câu tiếp ›” nổi bật. Thêm một chạm mỗi câu.
  - (b) Giữ tự chuyển nhưng trễ khoảng 0,5 giây để thấy lựa chọn, kèm dòng “Đã chọn ý 2 cho câu 1 · Sửa” ở câu sau.
  - (c) Tự chuyển chỉ khi bấm phím số; chạm thì giữ nguyên.
- **Khuyến nghị:** (c). Người dùng bàn phím như P04 vẫn nhanh; người dùng chạm có thêm bước xác nhận.
- **Kiểm chứng:** trong thử nghiệm, người chạm nhầm tự phát hiện và sửa được mà không cần hỏi.

### V6. Vùng chạm nhỏ ở các điều khiển quan trọng · Trung bình · [Usability / tiếp cận]

- **Vị trí và bằng chứng [QS] (đo ở 375 px):**
  - Nút ‹ (lối thoát duy nhất khi học và thi, vì thanh tab bị ẩn): 17×30 px.
  - Ô số trong lưới đề: 30×30 px.
  - Nút “Đổi hạng”: 84×32 px.
- **Persona:** P22, P05, P03, P06.
- **Giải pháp:**
  - Nút quay lại tối thiểu 44×44 px, có chữ: “‹ Lộ trình”, “‹ Thi thử”, lấy theo `backTo`.
  - Lưới đề 6 cột trên màn hình hẹp hơn 480 px (ô khoảng 50 px).
- **Trade-off:** lưới đề cao hơn (5 hàng × 50 px với 30 câu; 8 hàng với 45 câu), đẩy câu hỏi xuống. Có thể thu lưới thành nút “Danh sách câu (12/30 đã làm)” mở ra khi cần.
- **Kiểm chứng:** đo kích thước ≥ 44 px; trong thử nghiệm không còn chạm nhầm ô bên cạnh.

### V7. Hai số câu cùng lúc trong bài thi · Trung bình · [Usability]

- **Vị trí:** màn thi và màn xem lại: “Câu 2 trong đề” và “Câu 11”.
- **Persona:** P09, P10, P13.
- **Giải pháp:** trong bài thi chỉ hiện “Câu 2/30”. Số trong bộ chỉ hiện ở màn xem lại, ghi rõ và mờ: “Câu 2/30 · số 11 trong bộ 600”.
- **Kiểm chứng:** người thử nói đúng mình đang ở câu mấy của đề.

### V8. Sai một câu điểm liệt là nút “Học tiếp” bị thay · Trung bình · [Usability]

- **Vị trí:** CTA Lộ trình (`home()`, `index.html:369`).
- **Bằng chứng [QS]:** sau 1 câu điểm liệt sai, CTA thành “Ưu tiên · Ôn lại 1 câu đang sai”; muốn học tiếp nhóm phải cuộn tới “Các chặng”.
- **Ảnh hưởng [GT]:** mạch học bị cắt liên tục ở chặng đầu, đúng lúc người mới sai nhiều nhất.
- **Persona:** P12, P01, P11.
- **Giải pháp:** giữ “Học tiếp · <nhóm>” làm nút chính. Thêm ngay dưới một nút phụ, viền đỏ: “Ưu tiên: ôn 2 câu điểm liệt đang sai”. Chỉ đẩy ôn câu sai lên nút chính khi chặng điểm liệt đã học hết một vòng.
- **Trade-off:** ít ép ôn câu sai ngay, nhưng câu sai vẫn được ôn ở vòng 2 (lộ trình đã dặn “làm hai vòng”).
- **Kiểm chứng:** người mới học hết nhóm đầu mà không phải cuộn tìm nhóm đang học.

### V9. Sổ tay tràn ngang trên điện thoại · Trung bình · [Usability]

- **Bằng chứng [QS]:** 6/6 bảng tràn ở 375 px; cột “Câu” nằm ngoài khung nhìn.
- **Persona:** P20, P13, P01.
- **Giải pháp:** dưới 480 px, hiển thị mỗi hàng thành một thẻ. Ví dụ:

  > **Ô tô (mọi loại), xe mô tô**
  > Đường đôi: **60 km/h** · Đường hai chiều: **50 km/h**
  > Câu 145, 146, 147, 148

  Hoặc đơn giản hơn: bỏ `min-width: 480px` và cho chữ xuống dòng.
- **Trade-off:** thẻ chiếm chiều dọc nhiều hơn; bỏ `min-width` thì cột hẹp, chữ xuống nhiều dòng. **Khuyến nghị:** thẻ cho các bảng có từ 4 cột trở lên.
- **Kiểm chứng:** ở 375 px không còn cuộn ngang; người thử đọc được số câu mà không vuốt.

### V10. Mô phỏng hỏi trước khi cho học · Trung bình · [Usability]

- **Vị trí:** Mô phỏng → Học theo nhóm (`simStudy()`).
- **Bằng chứng [QS]:** lần đầu gặp tình huống đã phải chọn 3 ý; đáp án đầy đủ (`simFull`) chỉ hiện sau khi trả lời đủ.
- **Persona:** P21, P12.
- **Giải pháp:** với tình huống chưa từng làm, hiện thẻ 4 ý trước (dùng lại `simFull`) với nút “Đã đọc, kiểm tra tôi”, rồi mới hỏi. Tình huống đã gặp thì hỏi ngay như hiện tại.
- **Trade-off:** thêm một chạm cho lần đầu; nhưng tránh “đoán rồi sửa”.
- **Kiểm chứng:** tỷ lệ đúng ở lần kiểm tra đầu tiên của người thử cao hơn so với khi đoán (đo trong buổi thử, không phải số đã có).

### V11. Nhận diện tên: không lưu tiến độ, ô đếm tĩnh · Thấp–Trung bình · [Usability]

- **Bằng chứng [QS]:** 120 câu liên tục, không lưu; ô đếm ngoài trang luôn là “120”.
- **Giải pháp:**
  - Chia vòng 20 câu, cuối vòng báo “Đúng 14/20”.
  - Ô đếm hiện số tên đã nhận đúng, ví dụ “38/120”.
- **Kiểm chứng:** thoát giữa chừng rồi vào lại vẫn thấy tiến độ.

### V12. Không cảnh báo sắp hết giờ; đồng hồ không đọc được bằng trình đọc màn hình · Trung bình · [Tiếp cận]

- **Bằng chứng [QS]:** `#timer` không có `aria-live`, không đổi màu, không có cảnh báo.
- **Persona:** P06, P10, P19.
- **Giải pháp:**
  - Khi còn 2 phút và 30 giây: đồng hồ chuyển đỏ.
  - Một vùng `aria-live="polite"` đọc “Còn 2 phút”. Chỉ đọc ở các mốc, không đọc mỗi giây.
- **Kiểm chứng:** VoiceOver đọc cảnh báo ở các mốc; người thử biết sắp hết giờ.

### V13. Ước tính “0%” và “10,3/30 câu đúng” khi chưa học gì · Thấp · [Usability]

- **Bằng chứng [QS]:** người mới vào thấy “0%” màu đỏ và “10,3/30”. Con số 10,3 là kỳ vọng nếu đoán ngẫu nhiên.
- **Ảnh hưởng [GT]:** dễ hiểu nhầm (“chưa học mà đúng 10 câu?”) hoặc nản.
- **Giải pháp:** khi đã thuộc dưới khoảng 20% số câu điểm liệt, thay hai ô này bằng: “Học xong 60 câu điểm liệt để xem ước tính khả năng đạt”.
- **Trade-off:** mất con số ngay từ đầu, nhưng con số đó chưa có ý nghĩa.

### V14. Tiến độ trộn giữa các hạng và giữa người dùng chung máy · Thấp · [Usability, đã công bố]

- **Bằng chứng [QS]:** đổi B → A1 vẫn mang câu sai từ đề B. Trang có báo “Tiến độ dùng chung giữa các hạng”.
- **Giải pháp:** không thêm chức năng. Ở dòng “Tiến độ chỉ lưu trên trình duyệt này”, thêm gợi ý: “Hai người dùng chung máy: mỗi người mở bằng một trình duyệt (hoặc cửa sổ riêng) để tiến độ không lẫn.”

### V15. Câu trước: mất phản hồi đã trả lời, cho trả lời lại · Thấp · [Usability]

- **Bằng chứng [QS]:** sau khi trả lời câu 19 rồi bấm “Câu trước”, câu hiện trắng, trả lời lại được và được ghi thêm một lượt.
- **Giải pháp:** nhớ lựa chọn trong phiên; quay lại thì hiện lại phản hồi cũ, có nút “Làm lại câu này”.

---

## 6. Ưu tiên cải thiện

### Sửa nhanh (vài dòng mã hoặc chữ, ít rủi ro)

| Thứ tự | Vấn đề | Việc cần làm |
|---|---|---|
| 1 | V2 | Không `mark()` câu bỏ trống khi nộp bài |
| 2 | V1 | Thêm dòng “Trước đây: …” và câu dẫn về đổi tên hạng (sau khi đối chiếu văn bản) |
| 3 | V6 | Nút quay lại 44×44 có chữ; lưới 6 cột dưới 480 px |
| 4 | V7 | Bỏ số câu trong bộ khỏi màn thi |
| 5 | V12 | Đồng hồ đổi màu ở 2 phút và 30 giây; `aria-live` theo mốc |
| 6 | V4 (tạm) | Sửa lời dẫn Sổ tay nếu chưa làm liên kết |
| 7 | V13, V14 | Đổi câu chữ |
| 8 | V9 (tạm) | Bỏ `min-width` của bảng Sổ tay |

### Cần thiết kế hoặc thử nghiệm trước khi làm

| Vấn đề | Lý do cần thiết kế |
|---|---|
| V3 Quy tắc liên quan trong phản hồi | Cần quyết định vị trí, độ dài và phạm vi phủ |
| V4 Mở câu theo số | Thêm route; quyết định nơi đặt liên kết |
| V5 Tương tác chọn đáp án khi thi | Có trade-off tốc độ ↔ an toàn; nên thử A/B với người thật |
| V8 Logic nút chính Lộ trình | Ảnh hưởng toàn bộ mạch học |
| V9 Bảng thành thẻ trên điện thoại | Bố cục mới |
| V10 Học trước khi hỏi ở Mô phỏng | Thêm một bước trong luồng |
| V11, V15 | Lưu thêm trạng thái |

Không đề xuất tài khoản hay đồng bộ nhiều thiết bị (P24). Trang đã báo trước giới hạn này. Chỉ nên cân nhắc nếu thử nghiệm cho thấy đây là lý do bỏ cuộc phổ biến.

---

## 7. Kế hoạch kiểm chứng với người dùng thật

**Hình thức:** thử nghiệm có điều phối, từng người, trên điện thoại của chính họ; nói to suy nghĩ; 30–40 phút. Hai vòng: trước khi sửa (đo nền) và sau khi sửa nhanh. Mỗi vòng 6–8 người.

**Nhóm cần tuyển**

| Nhóm | Số người mỗi vòng | Lý do |
|---|---|---|
| Sắp thi B, chưa học, được dặn theo tên cũ (“B2”, “B1 số tự động”) | 2 | V1, V3, V8 |
| Sắp thi A1 hoặc A, có người đi xe máy điện | 1–2 | V1 (kW) |
| Nâng hạng C, D, CE, quen phần mềm của trung tâm | 1 | V5, V7 |
| Ít dùng web, để cỡ chữ lớn hoặc hay chạm nhầm | 1 | V5, V6 |
| Dùng trình đọc màn hình | 1 | V12, tiếp cận chung |
| Giáo viên trung tâm đào tạo lái xe | 1 | V4, độ đúng của Sổ tay |

**Tác vụ và dấu hiệu thành công**

| Tác vụ | Câu giao (không gợi ý tên nút) | Dấu hiệu thành công |
|---|---|---|
| Chọn hạng | “Trung tâm bảo bạn thi B2 / B1 số tự động. Hãy bắt đầu ôn.” | Chọn đúng B, không quay lại đổi |
| Học và hiểu khi sai | “Học 5 câu đầu. Câu nào sai, nói cho tôi vì sao đáp án kia đúng.” | Giải thích được nội dung quy tắc, không chỉ “vì ý 2” |
| Thi thử, sửa chạm nhầm | “Làm đề, ở câu 3 hãy đổi ý sau khi đã chọn.” | Sửa được mà không cần hỏi; biết đã lưu |
| Nộp sớm | “Làm 3 câu rồi nộp, sau đó xem phần Câu sai.” | Hiểu danh sách Câu sai; không ngạc nhiên vì số câu |
| Mở câu theo số | “Thầy dặn xem lại câu 145.” | Mở được trong ≤ 2 thao tác (sau khi sửa V4) |
| Tra Sổ tay | “Tốc độ tối đa của ô tô trên đường đôi trong khu dân cư? Câu nào hỏi việc này?” | Trả lời đúng cả hai, không vuốt ngang |
| Học tiếp | Đóng trang, mở lại: “Học tiếp từ chỗ bạn dừng.” | Một chạm vào đúng nhóm đang học |
| Mô phỏng (hạng ô tô) | “Học 3 tình huống đầu rồi làm kiểm tra thử.” | Không phàn nàn phải đoán; biết tiến độ |

**Ghi lại mỗi buổi:** chỗ dừng lại hoặc hỏi, thao tác sai, câu nói nguyên văn, hoàn thành hay không. Chỉ so sánh trước và sau trong cùng nhóm nhỏ, không suy ra tỷ lệ chung cho mọi người dùng.
