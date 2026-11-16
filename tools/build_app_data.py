#!/usr/bin/env python3
"""Gộp dữ liệu cho trang web và chạy các kiểm tra chất lượng.

Đầu vào : data/questions.json, data/critical.json, data/groups.json, data/notes.json, data/sim.json, data/videos.json, data/classes.json
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
CL = load("classes.json")
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
    # qchecks: nhãn của dòng (vd. hạng xe) phải khớp nội dung chính câu hỏi được dẫn, không chỉ đáp án
    for qid, needle in sec.get("qchecks", []):
        if needle not in byid[qid]["q"]: err.append(f"Sổ tay '{sec['title']}': đề câu {qid} không chứa “{needle}”")
    # trang lọc cột "Câu" theo bộ câu của từng hạng, nên ô phải là số, khoảng "a–b" hoặc danh sách cách nhau bởi dấu phẩy
    if sec.get("head") and "Câu" in sec["head"]:
        qc = sec["head"].index("Câu")
        for r in sec["rows"]:
            if not re.fullmatch(r"\s*\d+(\s*[–-]\s*\d+)?(\s*,\s*\d+(\s*[–-]\s*\d+)?)*\s*", r[qc]): err.append(f"Sổ tay '{sec['title']}': ô Câu không đọc được: {r[qc]}")

# 4. mô phỏng
if len(sim) != 120 or any(not all(s[k] for k in "ngtx") for s in sim): err.append("Dữ liệu mô phỏng phải đủ 120 tình huống, 4 trường")
videos = load("videos.json")["videos"]
for k, v in videos.items():
    if not (k.isdigit() and 1 <= int(k) <= 120 and re.fullmatch(r"[\w-]{11}", v)): err.append(f"videos.json: mục lỗi {k}: {v}")

# 5. hạng bằng lái: bộ câu, câu điểm liệt, cấu trúc đề (Công văn 2262/CSGT-P5, Thông tư 12/2025/TT-BCA)
CAT = {"rule": {1}, "culture": {2}, "tech": {3}, "struct": {4}, "techStruct": {3, 4}, "sign": {5}, "sh": {6}}
SIZE = {"A": (250, 20), "B1": (300, 30)}
for name, pl in CL["pools"].items():
    if (len(set(pl["ids"])), len(set(pl["crit"]))) != SIZE.get(name): err.append(f"Bộ câu {name}: sai số câu/điểm liệt")
    if not set(pl["crit"]) <= set(pl["ids"]) or not set(pl["crit"]) <= set(crit): err.append(f"Bộ câu {name}: câu điểm liệt nằm ngoài bộ hoặc ngoài 60 câu")
    if not set(pl["ids"]) <= set(byid): err.append(f"Bộ câu {name}: số câu ngoài 1–600")
for c in CL["classes"]:
    ids, cr = (range(1, 601), crit) if c["pool"] == "all" else (CL["pools"][c["pool"]]["ids"], CL["pools"][c["pool"]]["crit"])
    if sum(n for _, n in c["slots"]) != c["n"] or not 0 < c["pass"] <= c["n"]: err.append(f"Hạng {c['code']}: tổng câu/điểm đạt sai")
    for cat, n in c["slots"]:
        have = len(cr) if cat == "crit" else sum(1 for i in ids if byid[i]["ch"] in CAT[cat] and i not in cr)
        if have < n: err.append(f"Hạng {c['code']}: nhóm {cat} chỉ có {have} câu, cần {n}")

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
       "notes": [{k: v for k, v in s.items() if k not in ("checks", "qchecks")} for s in notes],
       "pools": CL["pools"], "classes": CL["classes"]}
(ROOT / "data" / "app.json").write_text(json.dumps(app, ensure_ascii=False, separators=(",", ":")))
print(f"Kiểm tra đạt. {len(Q)} câu, {len(traps)} câu bẫy, {len(groups['twins'])} chùm song sinh, {len(sim)} tình huống mô phỏng, {len(CL['classes'])} hạng bằng.")
