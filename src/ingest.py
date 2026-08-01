"""FWC Unfair Dismissal Decisions ingestion pipeline.

Structure-aware paragraph chunking for FWC decisions.
Reads .txt files from data/fwc_decisions/, chunks by decision structure.
"""
import os
import re
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict
from langchain_core.documents import Document


CORPUS_VERSION = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_fwc_decision(text: str, filename: str) -> Dict:
    """Parse an FWC decision into structured sections.
    
    FWC decisions typically have:
    - Header (decision number, date, member)
    - Background/history
    - Issues
    - Conclusion
    - Orders
    """
    sections = []
    
    # Try to extract decision metadata from header
    metadata = {
        "decision_number": "",
        "decision_date": "",
        "member": "",
        "applicant": "",
        "respondent": "",
    }
    
    # Extract decision number (e.g., [2024] FWC 1234)
    num_match = re.search(r'\[(\d{4})\]\s*FWC\s*(\d+)', text)
    if num_match:
        metadata["decision_number"] = f"[{num_match.group(1)}] FWC {num_match.group(2)}"
    
    # Extract date
    date_match = re.search(r'Date.*?(\d{1,2})\s*(\w+)\s*(\d{4})', text[:2000])
    if date_match:
        metadata["decision_date"] = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}"
    
    # Extract member name
    member_match = re.search(r'(?:Decision|Determination)\s+of\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', text[:2000])
    if member_match:
        metadata["member"] = member_match.group(1)
    
    # Split by common FWC decision headings
    heading_pattern = re.compile(
        r'^(?:Background|History|Issues|Conclusion|Orders?|Decision|Determination|'
        r'Remedy|Compensation|Reinstatement|Jurisdiction|Introduction|'
        r'Is the dismissal harsh|Was there a valid reason|Summary dismissal|'
        r'What is an unfair dismissal|Minimum employment period|'
        r'High income threshold|Extension of time)\s*$',
        re.MULTILINE | re.IGNORECASE
    )
    
    # Split text into sections
    parts = heading_pattern.split(text)
    
    for i, part in enumerate(parts):
        part = part.strip()
        if not part or len(part) < 50:
            continue
        
        # Find the heading that precedes this part
        heading_match = heading_pattern.search(text, text.find(part) if part in text else 0)
        heading = heading_match.group(0).strip() if heading_match else f"Section {i}"
        
        sections.append({
            "heading": heading,
            "text": part,
        })
    
    # If no sections found, treat whole document as one section
    if not sections:
        sections.append({
            "heading": "Full Decision",
            "text": text,
        })
    
    return {
        "metadata": metadata,
        "sections": sections,
        "filename": filename,
    }


def chunk_section(text: str, max_chunk_size: int = 1500) -> List[str]:
    """Split section text into chunks, preserving paragraph boundaries."""
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    paragraphs = text.split('\n\n')
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if len(para) > max_chunk_size:
                # Split long paragraphs by sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current_chunk = ""
                for sent in sentences:
                    if len(current_chunk) + len(sent) + 1 <= max_chunk_size:
                        current_chunk += sent + " "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sent + " "
            else:
                current_chunk = para + "\n\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def decision_to_documents(decision_path: str) -> List[Document]:
    """Convert an FWC decision file to LangChain Documents."""
    filename = os.path.basename(decision_path)
    
    with open(decision_path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    parsed = parse_fwc_decision(text, filename)
    documents = []
    
    # Compute source hash
    source_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    
    for section in parsed["sections"]:
        chunks = chunk_section(section["text"])
        
        for i, chunk in enumerate(chunks):
            metadata = {
                "document_type": "FWC_Decision",
                "source_file": filename,
                "decision_number": parsed["metadata"]["decision_number"],
                "decision_date": parsed["metadata"]["decision_date"],
                "member": parsed["metadata"]["member"],
                "section_heading": section["heading"],
                "chunk_index": i,
                "source_version": CORPUS_VERSION,
                "source_hash": source_hash,
            }
            
            # Contextual prefix for better retrieval
            prefix = f"[FWC Decision {parsed['metadata']['decision_number']} - {section['heading']}] "
            contextualized = prefix + chunk
            
            documents.append(Document(page_content=contextualized, metadata=metadata))
    
    return documents


def ingest_fwc_decisions(decisions_dir: str = "data/fwc_decisions") -> List[Document]:
    """Ingest all FWC decision files from directory."""
    decisions_path = Path(decisions_dir)
    
    if not decisions_path.exists():
        print(f"Decisions directory not found: {decisions_dir}")
        return []
    
    # Find all .txt files
    txt_files = sorted(decisions_path.glob("*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {decisions_dir}")
        print("Please download FWC decisions manually from:")
        print("  https://www.fwc.gov.au/document-search?search-ui=decisions")
        print("  Search: 'unfair dismissal', Type: Decisions, Date: 01/01/2023 - 31/07/2026")
        return []
    
    print(f"Found {len(txt_files)} decision files")
    
    all_docs = []
    errors = []
    
    for idx, txt_file in enumerate(txt_files):
        try:
            docs = decision_to_documents(str(txt_file))
            all_docs.extend(docs)
            if (idx + 1) % 10 == 0:
                print(f"  [{idx+1}/{len(txt_files)}] {txt_file.name}: {len(docs)} chunks")
        except Exception as e:
            errors.append((txt_file.name, str(e)))
            print(f"  ERROR {txt_file.name}: {e}")
    
    print(f"\nIngested: {len(all_docs)} chunks from {len(txt_files)} decisions")
    if errors:
        print(f"Errors: {len(errors)} files failed")
    
    # Deduplicate
    seen = set()
    unique_docs = []
    for doc in all_docs:
        content_hash = hashlib.md5(doc.page_content.encode('utf-8')).hexdigest()
        if content_hash not in seen:
            seen.add(content_hash)
            unique_docs.append(doc)
    
    if len(unique_docs) < len(all_docs):
        print(f"Deduplicated: {len(all_docs)} -> {len(unique_docs)} chunks")
    
    return unique_docs


def ingest_legislation(legislation_path: str = "data/legislation/fair_work_act_s385_394.txt") -> List[Document]:
    """Ingest Fair Work Act legislation text."""
    if not os.path.exists(legislation_path):
        print(f"Legislation file not found: {legislation_path}")
        return []
    
    with open(legislation_path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    documents = []
    
    # Split by section numbers (385, 386, etc.) - bare format without "Section" prefix
    section_pattern = re.compile(r'^(\d{3}[A-Z]?\s+.+)$', re.MULTILINE)
    parts = section_pattern.split(text)
    
    # Process: parts[0] is preamble, then alternating: section_header, section_content
    preamble = parts[0].strip()
    if preamble and len(preamble) > 100:
        chunks = chunk_section(preamble)
        for j, chunk in enumerate(chunks):
            metadata = {
                "document_type": "Legislation",
                "source_file": "fair_work_act_s385_394.txt",
                "section_number": "Preamble",
                "section_heading": "Fair Work Act 2009 - Part 3-2 Division 4",
                "chunk_index": j,
                "source_version": CORPUS_VERSION,
                "source_url": "https://www.legislation.gov.au/C2009A00142",
            }
            prefix = "[Fair Work Act 2009 - Part 3-2 Division 4 - Unfair Dismissal] "
            documents.append(Document(page_content=prefix + chunk, metadata=metadata))
    
    for i in range(1, len(parts), 2):
        section_header = parts[i].strip() if i < len(parts) else ""
        section_content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        
        full_section = f"{section_header}\n\n{section_content}" if section_content else section_header
        
        # Extract section number (e.g., "385", "386", "387")
        sec_match = re.match(r'^(\d{3}[A-Z]?)', section_header)
        section_num = sec_match.group(1) if sec_match else ""
        
        chunks = chunk_section(full_section)
        
        for j, chunk in enumerate(chunks):
            metadata = {
                "document_type": "Legislation",
                "source_file": "fair_work_act_s385_394.txt",
                "section_number": section_num,
                "section_heading": section_header[:100],
                "chunk_index": j,
                "source_version": CORPUS_VERSION,
                "source_url": "https://www.legislation.gov.au/C2009A00142",
            }
            
            prefix = f"[Fair Work Act 2009 - s{section_num}] "
            documents.append(Document(page_content=prefix + chunk, metadata=metadata))
    
    print(f"Legislation: {len(documents)} chunks from s385-394")
    return documents


def ingest_all(awards_dir: str = "data/awards", nes_path: str = "data/nes/nes_combined.txt") -> List[Document]:
    """Legacy ingestion for Awards + NES (backward compatibility).
    
    Used by build_store.py and vectorstore.py.
    For new code, use ingest_fwc_decisions() + ingest_legislation() instead.
    """
    import glob as glob_mod
    
    documents = []
    
    # Ingest Awards (PDFs)
    if awards_dir and os.path.isdir(awards_dir):
        pdf_files = sorted(glob_mod.glob(os.path.join(awards_dir, "*.pdf")))
        if pdf_files:
            print(f"Found {len(pdf_files)} Award PDFs in {awards_dir}")
            # Try to use PyPDF2 for PDF ingestion
            try:
                from PyPDF2 import PdfReader
                for pdf_path in pdf_files:
                    filename = os.path.basename(pdf_path)
                    try:
                        reader = PdfReader(pdf_path)
                        for page_num, page in enumerate(reader.pages):
                            text = page.extract_text()
                            if text and len(text.strip()) > 50:
                                metadata = {
                                    "document_type": "Award",
                                    "source_file": filename,
                                    "page_number": page_num + 1,
                                }
                                documents.append(Document(
                                    page_content=text.strip(),
                                    metadata=metadata,
                                ))
                    except Exception as e:
                        print(f"  ERROR {filename}: {e}")
                print(f"Awards: {len(documents)} chunks from {len(pdf_files)} PDFs")
            except ImportError:
                print("WARNING: PyPDF2 not installed. Cannot ingest Award PDFs.")
    
    # Ingest NES
    if nes_path and os.path.exists(nes_path):
        with open(nes_path, encoding='utf-8', errors='replace') as f:
            nes_text = f.read()
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in nes_text.split('\n\n') if p.strip() and len(p.strip()) > 50]
        
        for i, para in enumerate(paragraphs):
            metadata = {
                "document_type": "NES",
                "source_file": "nes_combined.txt",
                "chunk_index": i,
            }
            documents.append(Document(
                page_content=f"[National Employment Standards] {para}",
                metadata=metadata,
            ))
        print(f"NES: {len(paragraphs)} chunks from nes_combined.txt")
    
    print(f"Total (legacy): {len(documents)} chunks")
    return documents


if __name__ == "__main__":
    # Ingest legislation
    leg_docs = ingest_legislation()
    
    # Ingest FWC decisions (if available)
    fwc_docs = ingest_fwc_decisions()
    
    all_docs = leg_docs + fwc_docs
    print(f"\nTotal: {len(all_docs)} chunks")
    
    # Summary by type
    types = {}
    for doc in all_docs:
        dtype = doc.metadata.get("document_type", "unknown")
        types[dtype] = types.get(dtype, 0) + 1
    print(f"By type: {types}")
