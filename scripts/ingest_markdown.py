#!/usr/bin/env python3
"""Fast ingestion from markdown files - much faster than PDF ingestion."""
import os
import re
from langchain_core.documents import Document


def parse_md_sections(md_content: str, award_name: str, source_file: str) -> list[dict]:
    """Parse markdown into sections based on headers."""
    sections = []
    current_section = None
    current_text = []
    
    for line in md_content.split('\n'):
        # Detect ## headers (Part/Schedule)
        if line.startswith('## '):
            if current_section and current_text:
                sections.append({
                    'title': current_section,
                    'text': '\n'.join(current_text),
                })
            current_section = line.replace('## ', '').strip()
            current_text = []
        # Detect ### headers (Clauses)
        elif line.startswith('### '):
            if current_section and current_text:
                sections.append({
                    'title': current_section,
                    'text': '\n'.join(current_text),
                })
            current_section = line.replace('### ', '').strip()
            current_text = []
        else:
            current_text.append(line)
    
    if current_section and current_text:
        sections.append({
            'title': current_section,
            'text': '\n'.join(current_text),
        })
    
    # If no sections found, use whole document
    if not sections:
        sections.append({
            'title': award_name,
            'text': md_content,
        })
    
    return sections


def extract_clause_number(section_title: str) -> str:
    """Extract clause number from section title."""
    clause_match = re.match(r'^(\d+[A-Z]*)\.\s', section_title)
    if clause_match:
        return clause_match.group(1)
    
    part_match = re.match(r'^Part (\d+[A-Z]*)', section_title)
    if part_match:
        return f"Part {part_match.group(1)}"
    
    schedule_match = re.match(r'^Schedule ([A-Z])', section_title)
    if schedule_match:
        return f"Schedule {schedule_match.group(1)}"
    
    return ""


def chunk_text(text: str, max_chunk_size: int = 1500) -> list[str]:
    """Split text into chunks."""
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
            current_chunk = para + "\n\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def md_to_documents(md_path: str) -> list[Document]:
    """Convert a markdown file to LangChain Documents."""
    with open(md_path) as f:
        content = f.read()
    
    # Extract award name — try multiple strategies
    award_name = None
    source_file = os.path.basename(md_path).replace('.md', '.pdf')
    
    # Strategy 1: Check manual overrides
    AWARD_OVERRIDES = {
        "clerk-award.md": "Clerks—Private Sector Award 2010",
        "workplace-relations-act-1996.md": None,  # Skip non-award files
    }
    if os.path.basename(md_path) in AWARD_OVERRIDES:
        award_name = AWARD_OVERRIDES[os.path.basename(md_path)]
        if award_name is None:
            return []  # Skip this file
    
    # Strategy 2: Look for "Award 20XX" in first 1000 chars (standalone line)
    if not award_name:
        for line in content[:2000].split('\n'):
            award_match = re.search(r'([A-Z][A-Za-z\s—\-]+Award\s+20\d{2})', line)
            if award_match:
                award_name = award_match.group(1).strip()
                break
    
    # Strategy 3: First # header (only if it contains "Award")
    if not award_name:
        header_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if header_match:
            header = header_match.group(1).strip()
            if 'award' in header.lower():
                award_name = header
    
    # Strategy 4: Extract from filename
    if not award_name:
        # clerk-award.md → Clerks Award
        name_part = source_file.replace('.pdf', '').replace('-', ' ').title()
        award_name = f"{name_part} Award 2020"
    
    sections = parse_md_sections(content, award_name, source_file)
    
    documents = []
    for section in sections:
        clause_num = extract_clause_number(section['title'])
        chunks = chunk_text(section['text'])
        
        for i, chunk in enumerate(chunks):
            # Contextual Retrieval: Prepend context
            award_short = award_name.replace(' Award 2020', '').replace(' Award 2010', '').replace(' Award 2015', '').replace(' Award 2016', '')
            context_prefix = f"[{award_short} - {section['title']}] "
            contextualized_chunk = context_prefix + chunk
            
            metadata = {
                'award_name': award_name,
                'clause_number': clause_num,
                'section_title': section['title'],
                'source_url': f"https://www.fairwork.gov.au/employment-conditions/awards",
                'document_type': 'Award',
                'source_file': source_file,
                'chunk_index': i,
            }
            documents.append(Document(page_content=contextualized_chunk, metadata=metadata))
    
    return documents


def nes_md_to_documents(md_path: str) -> list[Document]:
    """Convert NES markdown to Documents."""
    with open(md_path) as f:
        content = f.read()
    
    documents = []
    sections = re.split(r'\n## (.+?)\n', content)
    
    for i in range(1, len(sections), 2):
        section_name = sections[i].strip()
        section_text = sections[i + 1].strip() if i + 1 < len(sections) else ""
        
        if not section_text:
            continue
        
        chunks = chunk_text(section_text)
        for j, chunk in enumerate(chunks):
            clause_refs = re.findall(r'clause[s]?\s+(\d+[A-Z]*(?:\.\d+)?)', chunk.lower())
            
            context_prefix = f"[National Employment Standards - {section_name}] "
            contextualized_chunk = context_prefix + chunk
            
            metadata = {
                'award_name': 'National Employment Standards',
                'clause_number': ', '.join(clause_refs) if clause_refs else section_name,
                'section_title': section_name,
                'source_url': 'https://www.fairwork.gov.au/employment-conditions/national-employment-standards',
                'document_type': 'NES',
                'source_file': 'nes_combined.md',
                'chunk_index': j,
            }
            documents.append(Document(page_content=contextualized_chunk, metadata=metadata))
    
    return documents


def ingest_from_md(md_dir: str = "data/md_awards") -> list[Document]:
    """Ingest all markdown files."""
    all_docs = []
    
    md_files = sorted([f for f in os.listdir(md_dir) if f.endswith('.md')])
    print(f"Processing {len(md_files)} markdown files...")
    
    for idx, md_file in enumerate(md_files):
        md_path = os.path.join(md_dir, md_file)
        try:
            if md_file == "nes_combined.md":
                docs = nes_md_to_documents(md_path)
            else:
                docs = md_to_documents(md_path)
            all_docs.extend(docs)
            
            if (idx + 1) % 10 == 0:
                print(f"  [{idx+1}/{len(md_files)}] {md_file}: {len(docs)} chunks (total: {len(all_docs)})")
        except Exception as e:
            print(f"  ERROR {md_file}: {e}")
    
    print(f"\nTotal: {len(all_docs)} chunks from {len(md_files)} markdown files")
    return all_docs


if __name__ == "__main__":
    docs = ingest_from_md()
    
    # Show stats
    award_types = {}
    for doc in docs:
        dtype = doc.metadata['document_type']
        award_types[dtype] = award_types.get(dtype, 0) + 1
    print(f"\nDocument types: {award_types}")
    
    # Show sample
    if docs:
        print(f"\nSample chunk:")
        print(f"  Content: {docs[0].page_content[:150]}...")
