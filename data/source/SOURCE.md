# Nguồn tài liệu

## 600-cau-hoi.pdf

- Tài liệu: *600 câu hỏi dùng cho sát hạch lái xe cơ giới đường bộ*, Cục Cảnh sát giao thông – Bộ Công an, Hà Nội 2025. Ban hành kèm Công văn 2262/CSGT-P5 ngày 07/5/2025, áp dụng từ 01/6/2025.
- Bản trong repo: 186 trang, 6.062.495 byte, xuất từ Microsoft Word ngày 12/5/2025.
- SHA-256: `d473be679b53458a33acc52057f3a4fe532ea489e91d88fb86789073cd98a9c5`
- Lấy từ đâu: bản lưu công khai trong repo `anhvh6/LuatGiaothong` (`data/official-600.pdf`), repo này ghi nguồn là bản đăng trên HoaTieu: https://f.hoatieu.vn/data/pdf/2025/05/14/cau-hoi-thi-giay-phep-lai-xe.pdf
- Chưa đối chiếu byte-to-byte với bản trên csgt.vn. Nếu tải được bản từ Cục CSGT, thay file này, chạy `make data` và xem diff.

Đáp án đúng trong tài liệu là phần được gạch chân. Tài liệu không đánh dấu câu điểm liệt; danh sách 60 câu lấy từ Phụ lục III Công văn 2262/CSGT-P5 (xem `data/critical.json`), bản đăng tại https://cdn.thuvienphapluat.vn/uploads/tintuc/2025/05/12/CV-2262-trang-2.pdf

## sim.json

120 tình huống mô phỏng chép từ Phụ lục I, Thông tư 17/2026/TT-BXD ngày 29/4/2026 của Bộ Xây dựng: https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/17-bxd-kem.pdf
