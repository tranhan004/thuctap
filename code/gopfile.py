import glob
import os
import re

root = "output1.md"

TARGET_BOOKS = {
"/home/npquy/DeepSeek-OCR/DOTS_OCR/DotsOCR/output1.md/de-cuoi-ky-1-toan-11-nam-2025-2026-truong-thpt-nguyen-trai-da-nang ",
}

def page_key(path):
    m = re.search(r"_page_(\d+)", path)
    return int(m.group(1)) if m else 9999

for book in TARGET_BOOKS:
    book_path = os.path.join(root, book)
    if not os.path.isdir(book_path):
        print(f"⚠️ Không tìm thấy: {book}")
        continue

    pages = glob.glob(f"{book_path}/*_page_*.md")
    pages = [p for p in pages if not p.endswith("_nohf.md")]
    pages = sorted(pages, key=page_key)

    if not pages:
        print(f"⚠️ {book}: không có page hợp lệ")
        continue

    out_file = os.path.join(root, f"{book}_MERGED.md")

    with open(out_file, "w", encoding="utf-8") as out:
        for p in pages:
            with open(p, "r", encoding="utf-8") as f:
                out.write("\n\n")
                out.write(f.read())

    print(f"✅ {book}: gộp {len(pages)} trang")
