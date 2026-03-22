from docx import Document
import json

docx = r'C:\Users\mulug\OneDrive\Desktop\insa\linuxbasicsforhackers.docx'
doc = Document(docx)

lines = []
for p in doc.paragraphs:
    if p.text.strip():
        lines.append({'style': p.style.name, 'text': p.text.strip()})

with open(r'C:\Users\mulug\OneDrive\Desktop\insa\lfh_extract\content.json', 'w', encoding='utf-8') as f:
    json.dump(lines, f, ensure_ascii=False, indent=2)

print('Total paragraphs:', len(lines))
for x in lines[:120]:
    print(f'[{x["style"]}] {x["text"][:120]}')
