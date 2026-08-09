"""
Attempt to convert Week 4 markdown guide(s) to PDF using pandoc if installed.
Usage: python tools/generate_pdfs.py

The script will look for pandoc on PATH. If not found it will print instructions.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "week04" / "week4_full_guide.md"
PDF = ROOT / "week04" / "week4_full_guide.pdf"

if not MD.exists():
    print(f"Markdown file not found: {MD}")
    sys.exit(1)

pandoc = shutil.which("pandoc")
if pandoc:
    print(f"Found pandoc at: {pandoc}")
    cmd = [pandoc, str(MD), "-o", str(PDF)]
    try:
        subprocess.check_call(cmd)
        print(f"Wrote {PDF} ({PDF.stat().st_size} bytes)")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print("pandoc failed with exit code", e.returncode)
        sys.exit(e.returncode)
else:
    print("pandoc not found on PATH.")
    print("To install pandoc, visit: https://pandoc.org/installing.html")
    print("Or, open the markdown file in VS Code and use Print -> Save as PDF.")
    sys.exit(2)
