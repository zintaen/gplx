# Ôn lý thuyết lái xe mọi hạng (gplx)

Trang web tĩnh để ôn sát hạch lý thuyết cho cả 15 hạng giấy phép lái xe (A1, A, B1, B, C1, C, D1, D2, D, BE, C1E, CE, D1E, D2E, DE) từ bộ 600 câu hỏi của Cục CSGT (2025), kèm 120 tình huống mô phỏng (Thông tư 17/2026/TT-BXD) cho các hạng ô tô. Chạy trên GitHub Pages: https://zintaen.github.io/gplx/

## Tính năng

- Trang chủ cho chọn hạng. Mỗi hạng dùng đúng bộ câu của mình (A1, A: 250 câu; B1: 300 câu; các hạng ô tô: 600 câu), đúng danh sách câu điểm liệt (20, 30 hoặc 60) và đúng cấu trúc đề.

| Hạng | Bộ câu | Điểm liệt | Đề | Thời gian | Đạt |
| --- | --- | --- | --- | --- | --- |
| A1 | 250 | 20 | 25 | 19 phút | 21 |
| A | 250 | 20 | 25 | 19 phút | 23 |
| B1 | 300 | 30 | 25 | 19 phút | 23 |
| B | 600 | 60 | 30 | 20 phút | 27 |
| C1 | 600 | 60 | 35 | 22 phút | 32 |
| C | 600 | 60 | 40 | 24 phút | 36 |
| D1, D2, D, BE, C1E, CE, D1E, D2E, DE | 600 | 60 | 45 | 26 phút | 41 |

- Phân tích đề theo hạng: số câu mỗi nhóm trong đề và trong bộ, phần đã thuộc, số câu đúng dự kiến và khả năng đạt ước tính nếu thi ngay.
- Lộ trình thông minh: điểm liệt trước, rồi câu dễ nhầm (song sinh, bẫy “Cả … ý trên”), rồi các nhóm còn lại xếp theo số câu ra đề trên mỗi câu học. Nút “Học tiếp” ưu tiên câu điểm liệt đang sai.
- Thi thử đúng cấu trúc, thời gian và điểm đạt của từng hạng; một nửa số câu mỗi nhóm lấy từ câu chưa thuộc.
- Mô phỏng (hạng ô tô): học 4 ý của từng tình huống (tên, dấu hiệu gián tiếp, dấu hiệu trực tiếp, xử lý), luyện nhận diện tên, kiểm tra thử 10 tình huống chấm 0,25 điểm mỗi ý.
- Câu sai, sổ tay con số; mỗi câu có liên kết tới trang tương ứng trong PDF gốc.
- Tiến độ lưu trong `localStorage` của trình duyệt, không gửi đi đâu.

## Dữ liệu được tạo ra thế nào

| Tệp | Nguồn | Cách tạo |
| --- | --- | --- |
| `data/questions.json`, `assets/q/*.jpg` | PDF 600 câu (`data/source/`) | `tools/extract_600.py`: đọc chữ, đáp án = phương án gạch chân, cắt vùng hình |
| `data/critical.json` | Phụ lục III Công văn 2262/CSGT-P5 | nhập tay 60 số câu |
| `data/classes.json` | Công văn 2262/CSGT-P5 (Phụ lục I, II, mục II), Thông tư 12/2025/TT-BCA | bộ câu A1/A và B1, câu điểm liệt từng bộ, cấu trúc đề, thời gian, điểm đạt của 15 hạng; build kiểm tra số câu và đủ câu cho mọi nhóm |
| `data/sim.json` | Phụ lục I Thông tư 17/2026/TT-BXD | chép từ văn bản (480/480 trường khớp nguyên văn) |
| `data/videos.json` | YouTube, kênh “Ôn Thi Lái Xe - Lý thuyết & Mô phỏng” | đối chiếu thủ công cảnh quay với nội dung từng tình huống |
| `data/groups.json` | tự biên soạn | chủ đề điểm liệt, chùm song sinh |
| `data/notes.json` | tự biên soạn | sổ tay; mọi con số có `checks` đối chiếu với đáp án gốc |
| `data/app.json` | gộp các tệp trên | `tools/build_app_data.py` |

Bộ trích xuất tự dừng nếu không đủ 600 câu, có câu không có hoặc có hơn một phương án gạch chân, hay số câu điểm liệt khác 60. Khi phát triển, kết quả được đối chiếu với một bản chép độc lập: khớp cả 600 đáp án.

## Chạy trên máy

```sh
make serve          # mở http://localhost:8000
```

Trang tải dữ liệu bằng `fetch`, nên phải chạy qua máy chủ web, không mở trực tiếp `index.html`.

## Cập nhật dữ liệu

```sh
pip install -r requirements.txt
make data           # trích xuất lại từ PDF + kiểm tra + dựng data/app.json
git diff            # xem thay đổi trước khi commit
```

GitHub Actions trích xuất lại từ PDF ở mỗi lần push và chặn đăng nếu dữ liệu commit không khớp PDF hoặc kiểm tra không đạt.

Mỗi sáng thứ Hai, workflow `watch.yml` chạy `tools/watch_sources.py`: tải lại các văn bản nguồn trong `data/source/watch.json` và báo nếu văn bản bị thay (mã băm khác), đồng thời kiểm tra các video trong `data/videos.json` còn nhúng được. Lần chạy lỗi không chặn deploy, GitHub gửi email báo. Việc cập nhật dữ liệu theo văn bản mới vẫn làm tay.

## Đăng lên GitHub Pages

```sh
git init -b main && git add . && git commit -m "Trang ôn lý thuyết lái xe"
gh repo create <tên-repo> --public --source=. --push
```

Sau đó vào **Settings → Pages → Build and deployment → Source: GitHub Actions**. Workflow `.github/workflows/pages.yml` sẽ kiểm tra rồi đăng trang.

## Giới hạn

- **Video mô phỏng có cho 53/120 tình huống**, nhúng từ YouTube (kênh “Ôn Thi Lái Xe - Lý thuyết & Mô phỏng”, quay từ phần mềm v2.0.0), chỉ tải khi bấm xem. Phần mềm v2.0.0 khác Phụ lục I Thông tư 17/2026 ở nhiều tình huống (nhất là 80–120), nên chỉ gắn video khi cảnh quay khớp nội dung; danh sách ở `data/videos.json`. Không lưu video trong repo.
- Cục Đường bộ Việt Nam đang rà soát đáp án một số tình huống Chương 6 trong Thông tư 17/2026 (tin ngày 29/7/2026). Nếu khác với hướng dẫn của giáo viên, theo giáo viên.
- Từ 01/3/2027 cấu trúc đề và ngân hàng câu hỏi thay đổi (Thông tư 108/2026/TT-BCA; ví dụ hạng B lên 50 câu, 33 phút, đạt 45). Khi đó cần thay PDF và cập nhật `data/classes.json`.
- Ngưỡng đạt bài kiểm tra mô phỏng do cơ sở đào tạo quy định.
