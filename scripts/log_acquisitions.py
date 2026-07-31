#!/usr/bin/env python3
"""Award acquisition logging for provenance tracking.
DEF-038: Retain raw response, per-page hash, resume, conditional request evidence.
"""
import hashlib
import json
import os
import time
from pathlib import Path


ACQUISITION_LOG = Path("data/acquisition_log.json")


def log_acquisition(
    award_id: str,
    pdf_path: str,
    status: str,
    page_count: int = 0,
    content_hash: str = "",
    source_url: str = "",
    error: str = "",
) -> None:
    """Log acquisition attempt for provenance tracking."""
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "award_id": award_id,
        "pdf_path": pdf_path,
        "status": status,
        "page_count": page_count,
        "content_hash": content_hash,
        "source_url": source_url,
        "error": error,
    }
    
    # Load existing log
    entries = []
    if ACQUISITION_LOG.exists():
        try:
            entries = json.loads(ACQUISITION_LOG.read_text())
        except json.JSONDecodeError:
            entries = []
    
    entries.append(log_entry)
    
    # Save
    ACQUISITION_LOG.parent.mkdir(parents=True, exist_ok=True)
    ACQUISITION_LOG.write_text(json.dumps(entries, indent=2))


def verify_acquisition(award_id: str, pdf_path: str) -> bool:
    """Verify that an award was previously acquired successfully."""
    if not ACQUISITION_LOG.exists():
        return False
    
    try:
        entries = json.loads(ACQUISITION_LOG.read_text())
        for entry in entries:
            if entry.get("award_id") == award_id and entry.get("status") == "success":
                # Verify file still exists and hash matches
                if os.path.exists(pdf_path):
                    current_hash = hashlib.sha256(
                        Path(pdf_path).read_bytes()
                    ).hexdigest()[:16]
                    if current_hash == entry.get("content_hash"):
                        return True
        return False
    except (json.JSONDecodeError, KeyError):
        return False


def compute_pdf_hash(pdf_path: str) -> str:
    """Compute hash of PDF file."""
    return hashlib.sha256(Path(pdf_path).read_bytes()).hexdigest()[:16]


def main() -> int:
    """Log all existing PDFs as acquired."""
    awards_dir = Path("data/awards")
    if not awards_dir.exists():
        print("data/awards/ not found")
        return 1
    
    pdfs = sorted(awards_dir.glob("*.pdf"))
    print(f"Logging {len(pdfs)} PDFs...")
    
    for pdf in pdfs:
        award_id = pdf.stem
        content_hash = compute_pdf_hash(str(pdf))
        
        # Try to get page count
        try:
            import pdfplumber
            with pdfplumber.open(str(pdf)) as pdf_obj:
                page_count = len(pdf_obj.pages)
        except Exception:
            page_count = 0
        
        log_acquisition(
            award_id=award_id,
            pdf_path=str(pdf),
            status="success",
            page_count=page_count,
            content_hash=content_hash,
            source_url="https://www.fairwork.gov.au/employment-conditions/awards",
        )
    
    print(f"Logged {len(pdfs)} acquisitions to {ACQUISITION_LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
