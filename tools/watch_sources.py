#!/usr/bin/env python3
"""Kiểm tra hằng tuần những thứ nằm ngoài repo mà trang phụ thuộc vào.

1. Văn bản nguồn (data/source/watch.json): còn tải được và mã băm không đổi.
2. Video YouTube (data/videos.json): còn tồn tại và còn cho nhúng.

Thoát mã 1 nếu có mục cần xem lại, để GitHub Actions báo lỗi (và gửi email).
Chỉ dùng thư viện chuẩn.
"""
import hashlib, json, os, pathlib, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (gplx source watch)"}


def fetch(url, timeout=90):
    for attempt in range(3):  # mạng của máy chủ nhà nước đôi khi chập chờn: thử lại trước khi báo lỗi
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 2:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable: the last attempt always returns or raises")


problems, lines = [], []

for s in json.loads((ROOT / "data/source/watch.json").read_text())["sources"]:
    try:
        got = hashlib.sha256(fetch(s["url"])).hexdigest()
    except Exception as e:
        problems.append(f"Không tải được: {s['name']} ({e}) — {s['url']}")
        continue
    if got != s["sha256"]:
        problems.append(f"Văn bản đã thay đổi: {s['name']} — đọc lại và cập nhật {', '.join(s['used_by'])}, rồi sửa sha256 trong data/source/watch.json thành {got}")
    else:
        lines.append(f"OK  {s['name']}")

videos = json.loads((ROOT / "data/videos.json").read_text())["videos"]
dead = []
for sit, vid in videos.items():
    try:  # oEmbed trả 401/404 khi video bị xóa, để riêng tư hoặc tắt cho phép nhúng
        fetch("https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v=" + vid, timeout=30)
    except urllib.error.HTTPError as e:
        dead.append(f"tình huống {sit}: {vid} (HTTP {e.code})")
    except Exception as e:
        dead.append(f"tình huống {sit}: {vid} ({e})")
    time.sleep(0.3)
if dead:
    problems.append("Video không còn xem/nhúng được — gỡ hoặc thay trong data/videos.json: " + "; ".join(dead))
else:
    lines.append(f"OK  {len(videos)} video YouTube còn nhúng được")

report = "\n".join(["## Kiểm tra nguồn dữ liệu", *lines, *(f"CẦN XEM: {p}" for p in problems)])
print(report)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        f.write(report.replace("\n", "\n\n") + "\n")
sys.exit(1 if problems else 0)
