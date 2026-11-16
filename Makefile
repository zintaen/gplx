.PHONY: data check serve

# Trích xuất lại 600 câu từ PDF gốc rồi dựng dữ liệu cho trang (cần: pip install -r requirements.txt)
data:
	python3 tools/extract_600.py data/source/600-cau-hoi.pdf
	python3 tools/build_app_data.py

# Chỉ kiểm tra và dựng data/app.json (không cần PyMuPDF)
check:
	python3 tools/build_app_data.py

# Xem thử trên máy: http://localhost:8000
serve:
	python3 -m http.server 8000
