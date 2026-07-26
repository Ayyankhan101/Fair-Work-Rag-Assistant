#!/usr/bin/env python3
"""Rename PDFs with proper award names for better context."""
import os
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from ingest import extract_award_name_from_pdf


def sanitize_filename(name: str) -> str:
    """Sanitize award name for use as filename."""
    # Remove special characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    # Strip whitespace
    name = name.strip()
    return name


def main():
    awards_dir = Path("data/awards")
    temp_dir = Path("data/awards_temp")
    
    # Get existing PDFs
    existing_pdfs = {p.name for p in awards_dir.glob("*.pdf")}
    
    # Process temp PDFs
    renamed = 0
    skipped = 0
    errors = 0
    
    for pdf_path in temp_dir.glob("**/*.pdf"):
        if pdf_path.name in existing_pdfs:
            skipped += 1
            continue
        
        try:
            award_name = extract_award_name_from_pdf(str(pdf_path))
            if award_name and award_name != "Unknown Award":
                new_name = sanitize_filename(award_name) + ".pdf"
                new_path = awards_dir / new_name
                
                # Avoid overwriting
                if new_path.exists():
                    base = new_name[:-4]
                    for i in range(1, 100):
                        new_name = f"{base} ({i}).pdf"
                        new_path = awards_dir / new_name
                        if not new_path.exists():
                            break
                
                os.rename(str(pdf_path), str(new_path))
                renamed += 1
                print(f"  {pdf_path.name} -> {new_name}")
            else:
                # Copy with original name if can't extract
                import shutil
                dest = awards_dir / pdf_path.name
                if not dest.exists():
                    shutil.copy2(str(pdf_path), str(dest))
                    renamed += 1
                    print(f"  {pdf_path.name} (kept original name)")
                else:
                    skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR: {pdf_path.name}: {e}")
    
    print(f"\nRenamed: {renamed}, Skipped: {skipped}, Errors: {errors}")
    print(f"Total PDFs in awards: {len(list(awards_dir.glob('*.pdf')))}")


if __name__ == "__main__":
    main()
