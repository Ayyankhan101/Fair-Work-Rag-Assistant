#!/usr/bin/env python3
"""Convert all award PDFs to markdown files for faster ingestion."""
import os
import re
import pdfplumber

AWARDS_DIR = "data/awards"
MD_DIR = "data/md_awards"


def extract_award_name(pdf_path: str) -> str:
    """Extract award name from first page."""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0].extract_text()
        lines = first_page.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 5 and not line.startswith('MA') and not line.startswith('PR'):
                return line
        return lines[0].strip() if lines else "Unknown Award"


def pdf_to_markdown(pdf_path: str) -> str:
    """Convert PDF to markdown with proper formatting including tables."""
    award_name = extract_award_name(pdf_path)
    md_lines = [f"# {award_name}\n"]
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        md_lines.append("")
                        continue
                    
                    # Detect Part headers
                    if re.match(r'^Part \d+[A-Z]*[—–-]', line):
                        md_lines.append(f"\n## {line}\n")
                    # Detect Schedule headers
                    elif re.match(r'^Schedule [A-Z][—–-]', line):
                        md_lines.append(f"\n## {line}\n")
                    # Detect clause numbers (e.g., "15.1 Something")
                    elif re.match(r'^\d+[A-Z]*\.\d+\s', line):
                        md_lines.append(f"\n### {line}\n")
                    # Detect clause headers (e.g., "15. Title")
                    elif re.match(r'^\d+[A-Z]*\.\s+[A-Z]', line):
                        md_lines.append(f"\n### {line}\n")
                    else:
                        md_lines.append(line)
            
            # Extract tables and append as markdown tables
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue
                # Convert table to markdown format
                md_lines.append("")
                for row_idx, row in enumerate(table):
                    if row is None:
                        continue
                    # Clean cells
                    cells = [str(cell).strip() if cell else "" for cell in row]
                    md_lines.append("| " + " | ".join(cells) + " |")
                    # Add separator after header row
                    if row_idx == 0:
                        md_lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
                md_lines.append("")
    
    return "\n".join(md_lines)


def convert_all():
    """Convert all PDFs to markdown."""
    os.makedirs(MD_DIR, exist_ok=True)
    
    pdf_files = sorted([f for f in os.listdir(AWARDS_DIR) if f.endswith('.pdf')])
    print(f"Converting {len(pdf_files)} PDFs to markdown...")
    
    for idx, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(AWARDS_DIR, pdf_file)
        md_file = pdf_file.replace('.pdf', '.md')
        md_path = os.path.join(MD_DIR, md_file)
        
        try:
            md_content = pdf_to_markdown(pdf_path)
            with open(md_path, 'w') as f:
                f.write(md_content)
            
            if (idx + 1) % 10 == 0:
                print(f"  [{idx+1}/{len(pdf_files)}] {pdf_file} → {md_file}")
        except Exception as e:
            print(f"  ERROR {pdf_file}: {e}")
    
    print(f"\nDone! {len(pdf_files)} markdown files saved to {MD_DIR}/")
    
    # Also convert NES
    nes_path = "data/nes/nes_combined.txt"
    if os.path.exists(nes_path):
        md_nes_path = os.path.join(MD_DIR, "nes_combined.md")
        with open(nes_path) as f:
            nes_text = f.read()
        # Convert NES section headers to markdown
        nes_md = re.sub(r'=== (.+?) ===', r'## \1', nes_text)
        with open(md_nes_path, 'w') as f:
            f.write(f"# National Employment Standards\n\n{nes_md}")
        print(f"  NES converted → nes_combined.md")


if __name__ == "__main__":
    convert_all()
