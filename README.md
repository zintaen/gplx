# Ôn lý thuyết lái xe hạng B

Trang web tĩnh để ôn bộ 600 câu hỏi sát hạch lý thuyết (Cục CSGT, 2025) và 120 tình huống mô phỏng (Thông tư 17/2026/TT-BXD), chạy trên GitHub Pages.

## Tính năng

- Lộ trình ôn theo mức rủi ro, có nút “Học tiếp” tới nhóm chưa thuộc: 60 câu điểm liệt chia 7 chủ đề, 52 chùm câu song sinh dễ nhầm, 34 câu bẫy “Cả … ý trên”, sa hình, biển báo, phần còn lại.
- Thi thử 30 câu, 20 phút, đúng cấu trúc đề hạng B (8 quy tắc, 1 điểm liệt, 1 văn hóa, 1 kỹ thuật, 1 cấu tạo, 9 biển báo, 9 sa hình); đạt khi đúng từ 27 câu và không sai câu điểm liệt.
- Mô phỏng: học 4 ý của từng tình huống (tên, dấu hiệu gián tiếp, dấu hiệu trực tiếp, xử lý), luyện nhận diện tên, kiểm tra thử 10 tình huống chấm 0,25 điểm mỗi ý.
- Câu sai, sổ tay con số; mỗi câu có liên kết tới trang tương ứng trong PDF gốc.
- Tiến độ lưu trong `localStorage` của trình duyệt, không gửi đi đâu.

## Dữ liệu được tạo ra thế nào

| Tệp | Nguồn | Cách tạo |
| --- | --- | --- |
| `data/questions.json`, `assets/q/*.jpg` | PDF 600 câu (`data/source/`) | `tools/extract_600.py`: đọc chữ, đáp án = phương án gạch chân, cắt vùng hình |
| `data/critical.json` | Phụ lục III Công văn 2262/CSGT-P5 | nhập tay 60 số câu |
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

## Đăng lên GitHub Pages

```sh
git init -b main && git add . && git commit -m "Trang ôn lý thuyết lái xe hạng B"
gh repo create <tên-repo> --public --source=. --push
```

Sau đó vào **Settings → Pages → Build and deployment → Source: GitHub Actions**. Workflow `.github/workflows/pages.yml` sẽ kiểm tra rồi đăng trang.

## Giới hạn

- **Video mô phỏng có cho 53/120 tình huống**, nhúng từ YouTube (kênh “Ôn Thi Lái Xe - Lý thuyết & Mô phỏng”, quay từ phần mềm v2.0.0), chỉ tải khi bấm xem. Phần mềm v2.0.0 khác Phụ lục I Thông tư 17/2026 ở nhiều tình huống (nhất là 80–120), nên chỉ gắn video khi cảnh quay khớp nội dung; danh sách ở `data/videos.json`. Không lưu video trong repo.
- Cục Đường bộ Việt Nam đang rà soát đáp án một số tình huống Chương 6 trong Thông tư 17/2026 (tin ngày 29/7/2026). Nếu khác với hướng dẫn của giáo viên, theo giáo viên.
- Từ 01/3/2027 đề hạng B tăng lên 50 câu, 33 phút, đạt 45 câu, kèm ngân hàng câu hỏi mới (Thông tư 108/2026/TT-BCA). Khi đó cần thay PDF và cập nhật cấu trúc đề trong `index.html`.
- Ngưỡng đạt bài kiểm tra mô phỏng do cơ sở đào tạo quy định.
