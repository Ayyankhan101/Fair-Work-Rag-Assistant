"""PDF + NES ingestion pipeline for Fair Work Awards — optimized for 122+ PDFs."""
import os
import re
import json
import pdfplumber
from concurrent.futures import ProcessPoolExecutor, as_completed
from langchain_core.documents import Document


AWARD_URL_MAP = {
    '1': 'salt-industry-award-2020',
    '10': 'storage-services-and-wholesale-award-2020',
    '11': 'sugar-industry-award-2020',
    '12': 'supported-employment-services-award-2020',
    '13': 'surveying-award-2020',
    '14': 'telecommunications-services-award-2020',
    '15': 'telstra-award-2015',
    '17': 'timber-industry-award-2020',
    '18': 'transport-cash-in-transit-award-2020',
    '19': 'travelling-shows-award-2020',
    '2': 'seafood-processing-award-2020',
    '20': 'vehicle-repair-services-and-retail-award-2020',
    '22': 'victorian-government-schools-award-2016',
    '23': 'employees-award-2016',
    '24': 'victorian-local-government-award-2015',
    '25': 'victorian-public-service-award-2016',
    '26': 'victorian-state-government-agencies-award-2015',
    '27': 'minerals-award-2015',
    '28': 'waste-management-award-2020',
    '29': 'water-industry-award-2020',
    '3': 'seagoing-industry-award-2020',
    '30': 'wine-industry-award-2020',
    '31': 'wool-storage-sampling-and-testing-award-2020',
    '4': 'security-services-industry-award-2020',
    '5': 'silviculture-award-2020',
    '6': 'industry-award-2010',
    '7': 'sporting-organisations-award-2020',
    '9': 'stevedoring-industry-award-2020',
    'MA000003': 'fast-food-industry-award-2020',
    'MA000004': 'general-retail-industry-award-2020',
    'MA000005': 'hair-and-beauty-industry-award-2020',
    'MA000006': 'higher-education-industry-academic-staff-award-2020',
    'MA000007': 'higher-education-industry-general-staff-award-2020',
    'MA000008': 'horse-and-greyhound-training-award-2020',
    'MA000009': 'hospitality-industry-general-award-2020',
    'MA000026': 'graphic-arts-printing-and-publishing-award-2020',
    'MA000027': 'health-professionals-and-support-services-award-2020',
    'MA000028': 'horticulture-award-2020',
    'MA000029': 'joinery-and-building-trades-award-2020',
    'MA000061': 'gas-industry-award-2020',
    'MA000062': 'hydrocarbons-industry-upstream-award-2020',
    'MA000064': 'hydrocarbons-field-geologists-award-2020',
    'MA000067': 'journalists-published-media-award-2020',
    'MA000073': 'food-beverage-and-tobacco-manufacturing-award-2020',
    'MA000081': 'live-performance-award-2020',
    'MA000094': 'fitness-industry-award-2020',
    'MA000099': 'labour-market-assistance-industry-award-2020',
    'MA000101': 'gardening-and-landscaping-services-award-2020',
    'MA000105': 'funeral-industry-award-2020',
    'MA000111': 'fire-fighting-industry-award-2020',
    'MA000112': 'local-government-industry-award-2020',
    'MA000116': 'legal-services-award-2020',
    'ma000001': 'black-coal-mining-industry-award-2020',
    'ma000011': 'mining-industry-award-2020',
    'ma000012': 'pharmacy-industry-award-2020',
    'ma000013': 'racing-clubs-events-award-2020',
    'ma000014': 'racing-industry-ground-maintenance-award-2020',
    'ma000015': 'rail-industry-award-2020',
    'ma000018': 'aged-care-award-2010',
    'ma000019': 'banking-finance-and-insurance-award-2020',
    'ma000020': 'building-and-construction-general-on-site-award-2020',
    'ma000021': 'business-equipment-award-2020',
    'ma000022': 'cleaning-services-award-2020',
    'ma000023': 'contract-call-centres-award-2020',
    'ma000024': 'cotton-ginning-award-2020',
    'ma000030': 'market-and-social-research-award-2020',
    'ma000031': 'medical-practitioners-award-2020',
    'ma000032': 'mobile-crane-hiring-award-2020',
    'ma000033': 'nursery-award-2020',
    'ma000034': 'nurses-award-2020',
    'ma000035': 'pastoral-award-2020',
    'ma000036': 'plumbing-and-fire-sprinklers-award-2020',
    'ma000038': 'road-transport-and-distribution-award-2020',
    'ma000039': 'road-transport-long-distance-operations-award-2020',
    'ma000045': 'coal-export-terminals-award-2020',
    'ma000046': 'air-pilots-award-2020',
    'ma000047': 'aircraft-cabin-crew-award-2020',
    'ma000048': 'airline-operations-ground-staff-award-2020',
    'ma000049': 'airport-employees-award-2020',
    'ma000050': 'marine-towage-award-2020',
    'ma000051': 'port-authorities-award-2020',
    'ma000052': 'ports-harbours-and-enclosed-water-vessels-award-2020',
    'ma000054': 'asphalt-industry-award-2020',
    'ma000055': 'cement-lime-and-quarrying-award-2020',
    'ma000056': 'concrete-products-award-2020',
    'ma000057': 'premixed-concrete-award-2020',
    'ma000058': 'registered-and-licensed-clubs-award-2020',
    'ma000059': 'meat-industry-award-2020',
    'ma000060': 'aluminium-industry-award-2020',
    'ma000063-as-at-2020-04-12': 'passenger-vehicle-transportation-award-2010',
    'ma000065': 'professional-employees-award-2020',
    'ma000069': 'pharmaceutical-industry-award-2020',
    'ma000070': 'cemetery-industry-award-2020',
    'ma000072': 'oil-refining-and-manufacturing-award-2020',
    'ma000074': 'poultry-processing-award-2020',
    'ma000076': 'educational-services-schools-general-staff-award-2020',
    'ma000077': 'educational-services-teachers-award-2020',
    'ma000078': 'book-industry-award-2020',
    'ma000079': 'architects-award-2020',
    'ma000080': 'amusement-events-and-recreation-award-2020',
    'ma000083': 'commercial-sales-award-2020',
    'ma000085': 'dredging-industry-award-2020',
    'ma000086': 'maritime-offshore-oil-and-gas-award-2020',
    'ma000088': 'electrical-power-industry-award-2020',
    'ma000092': 'alpine-resorts-award-2020',
    'ma000093': 'marine-tourism-and-charter-vessels-award-2020',
    'ma000096': 'dry-cleaning-and-laundry-industry-award-2020',
    'ma000097': 'pest-control-industry-award-2020',
    'ma000098': 'ambulance-and-patient-transport-industry-award-2020',
    'ma000104': 'miscellaneous-award-2020',
    'ma000106': 'real-estate-industry-award-2020',
    'ma000108': 'professional-diving-industry-industrial-award-2020',
    'ma000109': 'professional-diving-industry-recreational-award-2020',
    'ma000110': 'corrections-and-detention-private-sector-award-2020',
    'ma000114': 'aquaculture-industry-award-2020',
    'ma000115': 'services-award-2020',
    'ma000117': 'mannequins-and-models-award-2020',
    'ma000118': 'animal-care-and-veterinary-services-award-2020',
    'ma000119': 'restaurant-industry-award-2020',
    'ma000120': 'childrens-services-award-2010',
    'ma000153': 'australian-government-industry-award-2016',
}

# Numbered PDFs → award name from content
NUMBERED_AWARD_SLUGS = {
    '1': 'salt-industry-award-2020',
    '2': 'seafood-processing-award-2020',
    '3': 'seagoing-industry-award-2020',
    '4': 'security-services-industry-award-2020',
    '5': 'silviculture-award-2020',
    '6': 'industry-award-2010',
    '7': 'sporting-organisations-award-2020',
    '9': 'stevedoring-industry-award-2020',
    '10': 'storage-services-and-wholesale-award-2020',
    '11': 'sugar-industry-award-2020',
    '12': 'supported-employment-services-award-2020',
    '13': 'surveying-award-2020',
    '14': 'telecommunications-services-award-2020',
    '15': 'telstra-award-2015',
    '17': 'timber-industry-award-2020',
    '18': 'transport-cash-in-transit-award-2020',
    '19': 'travelling-shows-award-2020',
    '20': 'vehicle-repair-services-and-retail-award-2020',
    '22': 'victorian-government-schools-award-2016',
    '23': 'employees-award-2016',
    '24': 'victorian-local-government-award-2015',
    '25': 'victorian-public-service-award-2016',
    '26': 'victorian-state-government-agencies-award-2015',
    '27': 'minerals-award-2015',
    '28': 'waste-management-award-2020',
    '29': 'water-industry-award-2020',
    '30': 'wine-industry-award-2020',
    '31': 'wool-storage-sampling-and-testing-award-2020',
}


def extract_award_name_from_pdf(pdf_path: str) -> str:
    """Extract award name from first page of PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0].extract_text()
        lines = first_page.split('\n')
        # First line is usually "MA000xxx", second line is the actual award name
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 5 and not line.startswith('MA') and not line.startswith('PR'):
                return line
        return lines[0].strip()


def get_award_slug(source_file: str) -> str:
    """Map source filename to Fair Work URL slug."""
    base = source_file.replace('.pdf', '')

    # Try ma000xxx mapping
    if base in AWARD_URL_MAP:
        return AWARD_URL_MAP[base]

    # Try numbered mapping
    if base in NUMBERED_AWARD_SLUGS:
        return NUMBERED_AWARD_SLUGS[base]

    # Fallback: use filename
    return base.lower()


def parse_pdf_structure(pdf_path: str) -> list[dict]:
    """Parse PDF into structured sections with clause detection."""
    sections = []
    award_name = extract_award_name_from_pdf(pdf_path)
    source_file = os.path.basename(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        page_texts = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                page_texts.append((page.page_number, text))
                full_text += text + "\n"

    # Split by Part headers and clause numbers
    part_pattern = re.compile(
        r'^(Part \d+[A-Z]*—\s*.+|Schedule [A-Z]\s*[—–-]\s*.+|\d+[A-Z]*\.\s+.+)',
        re.MULTILINE
    )

    lines = full_text.split('\n')
    current_section = None
    current_text = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        match = part_pattern.match(line_stripped)
        if match:
            if current_section and current_text:
                sections.append({
                    'title': current_section,
                    'text': '\n'.join(current_text),
                    'award_name': award_name,
                    'source_file': source_file,
                })
            current_section = line_stripped
            current_text = []
        else:
            current_text.append(line_stripped)

    if current_section and current_text:
        sections.append({
            'title': current_section,
            'text': '\n'.join(current_text),
            'award_name': award_name,
            'source_file': source_file,
        })

    if not sections:
        sections.append({
            'title': award_name,
            'text': full_text,
            'award_name': award_name,
            'source_file': source_file,
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
    """Split text into chunks, trying to break at paragraph boundaries."""
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


def pdf_to_documents(pdf_path: str) -> list[Document]:
    """Convert a PDF to LangChain Documents with metadata."""
    sections = parse_pdf_structure(pdf_path)
    documents = []
    slug = get_award_slug(os.path.basename(pdf_path))

    for section in sections:
        clause_num = extract_clause_number(section['title'])
        chunks = chunk_text(section['text'])

        for i, chunk in enumerate(chunks):
            metadata = {
                'award_name': section['award_name'],
                'clause_number': clause_num,
                'section_title': section['title'],
                'source_url': f"https://www.fairwork.gov.au/employment-conditions/awards/{slug}",
                'document_type': 'Award',
                'source_file': section['source_file'],
                'chunk_index': i,
            }
            documents.append(Document(page_content=chunk, metadata=metadata))

    return documents


def nes_text_to_documents(nes_path: str) -> list[Document]:
    """Convert NES text to LangChain Documents with metadata."""
    with open(nes_path) as f:
        text = f.read()

    documents = []
    sections = re.split(r'\n=== (.+?) ===\n', text)

    for i in range(1, len(sections), 2):
        section_name = sections[i].strip()
        section_text = sections[i + 1].strip() if i + 1 < len(sections) else ""

        if not section_text:
            continue

        chunks = chunk_text(section_text)
        for j, chunk in enumerate(chunks):
            clause_refs = re.findall(r'clause[s]?\s+(\d+[A-Z]*(?:\.\d+)?)', chunk.lower())

            metadata = {
                'award_name': 'National Employment Standards',
                'clause_number': ', '.join(clause_refs) if clause_refs else section_name,
                'section_title': section_name,
                'source_url': 'https://www.fairwork.gov.au/employment-conditions/national-employment-standards',
                'document_type': 'NES',
                'source_file': 'nes_combined.txt',
                'chunk_index': j,
            }
            documents.append(Document(page_content=chunk, metadata=metadata))

    return documents


def ingest_all(awards_dir: str, nes_path: str) -> list[Document]:
    """Ingest all PDFs and NES, return list of LangChain Documents."""
    all_docs = []

    pdf_files = sorted([f for f in os.listdir(awards_dir) if f.endswith('.pdf')])
    print(f"Processing {len(pdf_files)} PDFs...")

    # Sequential ingestion (multiprocessing with pdfplumber can be tricky)
    for idx, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(awards_dir, pdf_file)
        try:
            docs = pdf_to_documents(pdf_path)
            all_docs.extend(docs)
            if (idx + 1) % 10 == 0:
                print(f"  [{idx+1}/{len(pdf_files)}] {pdf_file}: {len(docs)} chunks (total: {len(all_docs)})")
        except Exception as e:
            print(f"  ERROR {pdf_file}: {e}")

    print(f"  [{len(pdf_files)}/{len(pdf_files)}] Done: {len(all_docs)} award chunks")

    # Process NES
    if os.path.exists(nes_path):
        print(f"Processing NES...")
        nes_docs = nes_text_to_documents(nes_path)
        all_docs.extend(nes_docs)
        print(f"  NES: {len(nes_docs)} chunks")

    print(f"\nTotal: {len(all_docs)} chunks from {len(pdf_files)} PDFs + NES")
    return all_docs


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    awards_dir = "data/awards"
    nes_path = "data/nes/nes_combined.txt"

    docs = ingest_all(awards_dir, nes_path)

    # Show summary
    award_types = {}
    for doc in docs:
        dtype = doc.metadata['document_type']
        award_types[dtype] = award_types.get(dtype, 0) + 1
    print(f"\nDocument types: {award_types}")

    # Show sample
    if docs:
        print(f"\nSample chunk:")
        print(f"  Award: {docs[0].metadata['award_name']}")
        print(f"  Clause: {docs[0].metadata['clause_number']}")
        print(f"  Section: {docs[0].metadata['section_title']}")
        print(f"  Type: {docs[0].metadata['document_type']}")
        print(f"  URL: {docs[0].metadata['source_url']}")
        print(f"  Text: {docs[0].page_content[:100]}...")
