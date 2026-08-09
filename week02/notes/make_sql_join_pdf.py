from pathlib import Path
import re

root = Path(r"C:\Users\nb442238\fintrust-cloud-portfolio")
md_path = root / "week02" / "notes" / "sql_join_reference.md"
out_path = root / "week02" / "notes" / "sql_join_reference.pdf"
text = md_path.read_text(encoding="utf-8")

lines = []
for raw in text.splitlines():
    line = raw.rstrip()
    if not line:
        lines.append("")
    elif line.startswith("# "):
        lines.append(line[2:].strip())
    elif line.startswith("## "):
        lines.append(line[3:].strip())
    elif line.startswith("### "):
        lines.append(line[4:].strip())
    elif line.startswith("```"):
        lines.append("")
    else:
        lines.append(line)

wrapped = []
for line in lines:
    if not line:
        wrapped.append("")
        continue
    if len(line) <= 90:
        wrapped.append(line)
    else:
        for part in re.findall(r".{1,90}", line):
            wrapped.append(part)

# Build a simple PDF by hand.
def pdf_escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

page_width = 612
page_height = 792
margin_left = 50
margin_top = 760
line_height = 12
max_lines = 55
content_lines = []
for idx, line in enumerate(wrapped[:max_lines]):
    y = margin_top - idx * line_height
    content_lines.append((line, y))

content_stream = "BT\n/F1 10 Tf\n50 760 Td\n(Week 2 Day 1 SQL JOIN Reference) Tj\n0 -14 Td\n(FinTrust portfolio reference) Tj\n"
for line, y in content_lines:
    content_stream += f"0 -14 Td\n({pdf_escape(line)}) Tj\n"
content_stream += "ET"

objects = []
objects.append("<< /Type /Catalog /Pages 2 0 R >>")
objects.append("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
objects.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>")
objects.append(f"<< /Length {len(content_stream.encode('latin-1'))} >>\nstream\n{content_stream}\nendstream")
objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

pdf = bytearray(b"%PDF-1.4\n")
offsets = []
for obj in objects:
    offsets.append(len(pdf))
    pdf.extend(obj.encode("latin-1"))
    pdf.extend(b"\nendobj\n")

xref_offset = len(pdf)
pdf.extend(f"xref\n0 {len(objects)+1}\n".encode("latin-1"))
pdf.extend(b"0000000000 65535 f \n")
for off in offsets:
    pdf.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
pdf.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin-1"))

out_path.write_bytes(pdf)
print(f"Created {out_path} ({out_path.stat().st_size} bytes)")
