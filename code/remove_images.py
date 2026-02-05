import re

input_md = "/home/npquy/DeepSeek-OCR/DOTS_OCR/DotsOCR/Final/toan11_MERGED.md"
output_md = "CD11_NO_IMAGE.md"

with open(input_md, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(
    r'!\[[^\]]*\]\(data:image[^)]*\)',
    '',
    content,
    flags=re.DOTALL
)

content = re.sub(r'\n{3,}', '\n\n', content)

with open(output_md, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Đã xóa toàn bộ ảnh base64 khỏi Markdown")
