#!/usr/bin/env python3
"""Gộp dữ liệu cho trang web và chạy các kiểm tra chất lượng.

Đầu vào : data/questions.json, data/critical.json, data/groups.json, data/notes.json, data/sim.json, data/videos.json
Đầu ra  : data/app.json
Dừng với mã lỗi nếu có kiểm tra không đạt (dùng trong GitHub Actions).
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
load = lambda n: json.loads((ROOT / "data" / n).read_text())
Q = load("questions.json")["questions"]
crit = load("critical.json")["ids"]
groups = load("groups.json")
notes = load("notes.json")
sim = load("sim.json")["situations"]
byid = {q["id"]: q for q in Q}
err = []

# 1. ngân hàng câu hỏi
if [q["id"] for q in Q] != list(range(1, 601)): err.append("Ngân hàng không đủ 600 câu theo thứ tự")
for q in Q:
    if not 0 <= q["c"] < len(q["a"]): err.append(f"Câu {q['id']}: đáp án không hợp lệ")
    for im in q["im"]:
        if not (ROOT / "assets" / "q" / im).exists(): err.append(f"Câu {q['id']}: thiếu hình {im}")
if sorted(q["id"] for q in Q if q["k"]) != sorted(crit): err.append("Cờ điểm liệt không khớp critical.json")

# 2. nhóm
theme_ids = [i for t in groups["critThemes"] for i in t["ids"]]
if sorted(theme_ids) != sorted(crit): err.append("Các chủ đề điểm liệt không phủ đúng 60 câu")
for t in groups["twins"]:
    if len(t["ids"]) < 2 or any(i not in byid for i in t["ids"]): err.append(f"Chùm song sinh lỗi: {t}")

# 3. sổ tay: mọi con số phải khớp đáp án gốc
for sec in notes:
    for qid, needle in sec.get("checks", []):
        ans = byid[qid]["a"][byid[qid]["c"]]
        if needle not in ans: err.append(f"Sổ tay '{sec['title']}': câu {qid} không chứa “{needle}” (đáp án: {ans})")

# 4. mô phỏng
if len(sim) != 120 or any(not all(s[k] for k in "ngtx") for s in sim): err.append("Dữ liệu mô phỏng phải đủ 120 tình huống, 4 trường")
videos = load("videos.json")["videos"]
for k, v in videos.items():
    if not (k.isdigit() and 1 <= int(k) <= 120 and re.fullmatch(r"[\w-]{11}", v)): err.append(f"videos.json: mục lỗi {k}: {v}")

# thống kê
CA = re.compile(r"^(Cả (hai|ba) ý trên|Ý \d và ý \d)")
ca = [q for q in Q if any(CA.match(a) for a in q["a"])]
traps = [q["id"] for q in ca if not CA.match(q["a"][q["c"]])]
plain = [q for q in Q if q not in ca and not q["im"]]
longest = sum(1 for q in plain if max(range(len(q["a"])), key=lambda i: len(q["a"][i])) == q["c"])

if err:
    print("KIỂM TRA KHÔNG ĐẠT:\n  " + "\n  ".join(err)); sys.exit(1)
app = {"Q": [{k: q[k] for k in ("id", "ch", "q", "a", "c", "k", "im", "page")} for q in Q],
       "traps": traps, "twins": groups["twins"], "critThemes": groups["critThemes"],
       "stats": {"caTotal": len(ca), "longPct": round(100 * longest / len(plain))},
       "notes": [{k: v for k, v in s.items() if k != "checks"} for s in notes]}
(ROOT / "data" / "app.json").write_text(json.dumps(app, ensure_ascii=False, separators=(",", ":")))
print(f"Kiểm tra đạt. {len(Q)} câu, {len(traps)} câu bẫy, {len(groups['twins'])} chùm song sinh, {len(sim)} tình huống mô phỏng.")
