import re
import json

LEVEL_MAP = {
    "Biết": "1",
    "Hiểu": "2",
    "VD": "3",
    "Vận dụng": "3"
}

# ---------- UTILS ----------
def split_questions(content):
    """
    Tách câu hỏi chịu được OCR xấu:
    **Câu 1**, **Câu 1.**, Câu 1:
    """
    return re.split(
        r"(?:\*\*)?\s*Câu\s+(\d+)\s*[:\.]?\s*(?:\*\*)?",
        content,
        flags=re.IGNORECASE
    )

# ---------- PHẦN I ----------
def parse_part_1(content):
    results = []
    blocks = split_questions(content)

    for i in range(1, len(blocks), 2):
        q_num = blocks[i]
        q_body = blocks[i + 1]

        main_content = re.split(
            r"(?:Đáp án|Yêu cầu cần đạt)",
            q_body,
            maxsplit=1
        )[0].strip()

        answer_match = re.search(
            r"Đáp án\s*[:\-]?\s*([A-D0-9,\.]+)",
            q_body
        )
        answer = answer_match.group(1) if answer_match else ""

        level_match = re.search(
            r"(Biết|Hiểu|VD|Vận dụng)",
            q_body
        )
        level = LEVEL_MAP.get(level_match.group(1), "0") if level_match else "0"

        results.append({
            "section": "1",
            "level": level,
            "contents": f"Câu {q_num}. {main_content}",
            "answer": answer
        })

    return results

# ---------- PHẦN II ----------
def parse_part_2(content):
    results = []
    blocks = split_questions(content)

    for i in range(1, len(blocks), 2):
        q_num = blocks[i]
        q_body = blocks[i + 1]

        main_content = re.split(
            r"(?:Đáp án|Yêu cầu cần đạt)",
            q_body,
            maxsplit=1
        )[0].strip()

        # giữ a) b) c) d)
        main_content = re.sub(
            r"\n?\s*([a-d])\)",
            r"\n\n\1)",
            main_content,
            flags=re.IGNORECASE
        )

        answers = re.findall(r"([a-d])\)\s*([DS])", q_body)
        answer = ",".join(a[1] for a in answers)

        levels = re.findall(r"(Biết|Hiểu|VD|Vận dụng)", q_body)
        level = ",".join(LEVEL_MAP.get(lv, "0") for lv in levels)

        results.append({
            "section": "2",
            "level": level,
            "contents": f"Câu {q_num}. {main_content}",
            "answer": answer
        })

    return results

# ---------- PHẦN III ----------
def parse_part_3(content):
    results = []
    blocks = split_questions(content)

    for i in range(1, len(blocks), 2):
        q_num = blocks[i]
        q_body = blocks[i + 1]

        main_content = re.split(
            r"Yêu cầu cần đạt",
            q_body,
            maxsplit=1
        )[0].strip()

        level_match = re.search(
            r"(Biết|Hiểu|VD|Vận dụng)",
            q_body
        )
        level = LEVEL_MAP.get(level_match.group(1), "0") if level_match else "0"

        results.append({
            "section": "3",
            "level": level,
            "contents": f"Câu {q_num}. {main_content}",
            "answer": ""
        })

    return results

# ---------- MAIN ----------
def parse_markdown(md_text):
    all_results = []

    part_1 = re.search(
        r"PHẦN\s*I[\s\S]*?(?=PHẦN\s*II)",
        md_text,
        re.IGNORECASE
    )
    part_2 = re.search(
        r"PHẦN\s*II[\s\S]*?(?=PHẦN\s*III)",
        md_text,
        re.IGNORECASE
    )
    part_3 = re.search(
        r"PHẦN\s*III[\s\S]*",
        md_text,
        re.IGNORECASE
    )

    if part_1:
        all_results.extend(parse_part_1(part_1.group()))
    if part_2:
        all_results.extend(parse_part_2(part_2.group()))
    if part_3:
        all_results.extend(parse_part_3(part_3.group()))

    return all_results

# ---------- RUN ----------
if __name__ == "__main__":
    with open(
        "/home/npquy/DeepSeek-OCR/DOTS_OCR/DotsOCR/output_FINAL1.md/12_LQĐ.md",   # ⚠️ PHẢI LÀ FILE .md
        "r",
        encoding="utf-8"
    ) as f:
        md_text = f.read()

    data = parse_markdown(md_text)

    with open("questions_all_parts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Parse xong {len(data)} câu")
