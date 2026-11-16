#!/usr/bin/env python3
"""Trích xuất bộ 600 câu hỏi sát hạch lái xe từ PDF gốc của Cục CSGT.

- Câu hỏi: dòng in đậm bắt đầu bằng "Câu N.".
- Phương án: "1.", "2."... theo đúng thứ tự, có thể nằm giữa dòng.
- Đáp án: phương án có chữ được gạch chân (PDF vẽ gạch chân bằng hình chữ nhật đen rất mỏng).
- Hình: vùng nằm giữa đề bài và phương án đầu tiên, cắt nguyên vùng từ trang PDF.
- Câu điểm liệt: lấy từ Phụ lục III Công văn 2262/CSGT-P5 (data/critical.json), PDF không đánh dấu.

Cách dùng: python3 tools/extract_600.py data/source/600-cau-hoi.pdf
Kết quả: data/questions.json và assets/q/*.jpg. Script dừng với mã lỗi nếu kiểm tra không đạt.
"""
import json, re, sys, hashlib, pathlib
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "data" / "questions.json"
OUT_IMG = ROOT / "assets" / "q"
CHAPTERS = [(1, 180), (181, 205), (206, 263), (264, 300), (301, 485), (486, 600)]


def chapter_of(n):
    for i, (a, b) in enumerate(CHAPTERS, 1):
        if a <= n <= b:
            return i
    raise ValueError(n)


def underline_rects(page):
    rs = []
    for d in page.get_drawings():
        f = d.get("fill")
        r = d["rect"]
        if f is not None and max(f) < 0.2 and r.height <= 2.2 and r.width > 2:
            rs.append(r)
    return rs


def page_items(page):
    """Dòng chữ (kèm từng ký tự) và ảnh, sắp theo thứ tự đọc."""
    items = []
    raw = page.get_text("rawdict")
    for b in raw["blocks"]:
        if b["type"] == 1:
            items.append({"kind": "img", "bbox": pymupdf.Rect(b["bbox"])})
            continue
        for ln in b["lines"]:
            chars, bold = [], 0
            for sp in ln["spans"]:
                isb = "Bold" in sp["font"]
                for ch in sp["chars"]:
                    chars.append((ch["c"], pymupdf.Rect(ch["bbox"])))
                    if isb and ch["c"].strip():
                        bold += 1
            text = "".join(c for c, _ in chars)
            if not text.strip():
                continue
            nonspace = sum(1 for c, _ in chars if c.strip())
            items.append({"kind": "line", "chars": chars, "text": text,
                          "bbox": pymupdf.Rect(ln["bbox"]), "bold": bold >= 0.6 * max(nonspace, 1)})
    # ảnh không nằm trong luồng chữ: sắp theo tọa độ
    items.sort(key=lambda it: (round(it["bbox"].y0 / 3), it["bbox"].x0))
    return items


def is_underlined(rect, unders):
    h = rect.height
    for u in unders:
        ov = min(rect.x1, u.x1) - max(rect.x0, u.x0)
        if ov >= 0.5 * max(rect.width, 0.1) and rect.y0 + 0.55 * h <= u.y0 <= rect.y1 + 3.5:
            return True
    return False



def split_columns(chars, gap=24):
    """Tách một dòng thành các cột khi có khoảng trắng ngang lớn (phương án xếp 2 cột)."""
    segs, cur, last_x1 = [], [], None
    for c, r in chars:
        if c.strip():
            if last_x1 is not None and r.x0 - last_x1 > gap and cur:
                segs.append(cur)
                cur = []
            last_x1 = r.x1
        cur.append((c, r))
    if cur:
        segs.append(cur)
    return segs


def option_cuts(s, cur):
    """Vị trí bắt đầu phương án "k." trong đoạn: ở đầu đoạn, hoặc ngay sau dấu kết câu với k là số kế tiếp."""
    cuts, used = [], set(cur["opts"])
    for m in re.finditer(r"(\d)\.\s", s):
        num = int(m.group(1))
        if num in used or not 1 <= num <= 4:
            continue
        before = s[:m.start()]
        at_start = not before.strip()
        after_end = before.rstrip().endswith((".", "?", ":")) and num == max(used | {0}) + 1
        if at_start or (after_end and before[-1:].isspace()):
            cuts.append((m.start(), m.end(), num))
            used.add(num)
    return cuts


def main(pdf_path):
    pdf_path = pathlib.Path(pdf_path)
    doc = pymupdf.open(pdf_path)
    sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    qs, cur, state, started = [], None, None, False
    page_no_re = re.compile(r"^\s*\d{1,3}\s*$")
    q_re = re.compile(r"^\s*Câu\s+(\d+)\s*[.:]\s*")


    for pi, page in enumerate(doc):
        unders = underline_rects(page)
        for it in page_items(page):
            if it["kind"] == "img":
                if cur is not None:  # ảnh có thể nằm trên hoặc cạnh các phương án
                    cur["fig"].append((pi, it["bbox"]))
                continue
            text = it["text"]
            if text.strip().startswith("CHƯƠNG"):
                started = True
                continue
            if not started or page_no_re.match(text):
                continue
            m = q_re.match(text)
            expected = (cur["id"] + 1) if cur else 1
            if m and int(m.group(1)) == expected and it["bold"]:
                cur = {"id": expected, "page": pi + 1, "q": text[m.end():], "opts": {}, "last": None, "fig": []}
                qs.append(cur)
                state = "q"
                continue
            if cur is None:
                continue
            if it["bold"] and text.strip() == text.strip().upper() and re.search(r"[A-ZĐ]", text):
                continue  # dòng thứ hai của tiêu đề chương
            chars = it["chars"]
            segs = split_columns(chars)
            for seg in segs:
                s = "".join(c for c, _ in seg)
                cuts = option_cuts(s, cur)
                if state == "q" and not cuts:
                    if it["bold"]:
                        cur["q"] += " " + s
                    else:  # chú thích dưới hình: thuộc về vùng hình
                        cur["fig"].append((pi, it["bbox"]))
                    continue
                if cuts and cuts[0][0] > 0 and state == "q":
                    cur["q"] += " " + s[:cuts[0][0]]
                pos = cuts[0][0] if cuts else 0
                if cur["last"] is not None and pos > 0:
                    cur["opts"][cur["last"]] += [(c, r, is_underlined(r, unders)) for c, r in seg[:pos]]
                for idx, (a, b, num) in enumerate(cuts):
                    end = cuts[idx + 1][0] if idx + 1 < len(cuts) else len(seg)
                    cur["opts"][num] = [(c, r, is_underlined(r, unders)) for c, r in seg[b:end]]
                    cur["last"] = num
                    state = "o"
                if not cuts and cur["last"] is not None:
                    cur["opts"][cur["last"]] += [(" ", None, False)] + [(c, r, is_underlined(r, unders)) for c, r in seg]

    # ---- hậu xử lý, chấm đáp án, cắt hình ----
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    for f in OUT_IMG.glob("*.jpg"):
        f.unlink()
    crit = set(json.loads((ROOT / "data" / "critical.json").read_text())["ids"])
    out, errors = [], []
    clean = lambda t: re.sub(r"\s+", " ", t).strip()
    for q in qs:
        answers, ratios = [], []
        nums = sorted(q["opts"])
        if nums != list(range(1, len(nums) + 1)):
            errors.append(f"Câu {q['id']}: thứ tự phương án {nums}")
        for n in nums:
            o = q["opts"][n]
            txt = clean("".join(c for c, _, _ in o))
            vis = [u for c, r, u in o if c.strip()]
            answers.append(txt)
            ratios.append(sum(vis) / len(vis) if vis else 0)
        good = [i for i, r in enumerate(ratios) if r > 0.5]
        if len(good) != 1:
            errors.append(f"Câu {q['id']}: {len(good)} phương án gạch chân {[round(r, 2) for r in ratios]}")
        imgs = []
        if q["fig"]:
            by_page = {}
            for pi, r in q["fig"]:
                by_page.setdefault(pi, pymupdf.Rect(r))
                by_page[pi] |= r
            for k, (pi, r) in enumerate(sorted(by_page.items())):
                pg = doc[pi]
                clip = (r + (-2, -1, 2, 1)) & pg.rect
                if clip.height < 12:
                    continue
                pix = pg.get_pixmap(clip=clip, dpi=150)
                name = f"q{q['id']:03d}_{k + 1}.jpg"
                pix.save(OUT_IMG / name, jpg_quality=78)
                imgs.append(name)
        out.append({"id": q["id"], "ch": chapter_of(q["id"]), "q": clean(q["q"]), "a": answers,
                    "c": good[0] if len(good) == 1 else -1, "k": 1 if q["id"] in crit else 0,
                    "im": imgs, "page": q["page"]})
    ids = [q["id"] for q in out]
    if ids != list(range(1, 601)):
        errors.append(f"Số câu: {len(ids)}, thiếu {sorted(set(range(1, 601)) - set(ids))[:20]}")
    if sum(q["k"] for q in out) != 60:
        errors.append("Số câu điểm liệt khác 60")
    for q in out:
        if len(q["a"]) < 2:
            errors.append(f"Câu {q['id']}: chỉ có {len(q['a'])} phương án")
    OUT_JSON.write_text(json.dumps({"source": {"file": pdf_path.name, "sha256": sha},
                                    "questions": out}, ensure_ascii=False, indent=1))
    print(f"{len(out)} câu, {sum(len(q['im']) for q in out)} hình, sha256 {sha[:12]}…")
    if errors:
        print("LỖI KIỂM TRA:\n  " + "\n  ".join(errors[:60]))
        sys.exit(1)
    print("Kiểm tra đạt: đủ 600 câu, mỗi câu đúng một đáp án gạch chân, 60 câu điểm liệt.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "data" / "source" / "600-cau-hoi.pdf")
