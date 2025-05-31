import pdfplumber
from memory.memory_store import shared_memory


class PDFAgent:
    def __init__(self):
        pass

    def process(self, entry_id):
        # Fetch raw content from memory
        entry = shared_memory.retrieve(entry_id)
        if not entry:
            print(f"[PDFAgent] No entry found for ID: {entry_id}")
            return

        filepath = entry.get("source")
        if not filepath:
            print(f"[PDFAgent] No source file found in entry {entry_id}")
            return

        # Extract full text again from PDF (could improve caching later)
        with pdfplumber.open(filepath) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # For demo, we just count pages and word count as extracted info
        page_count = len(pdf.pages)
        word_count = len(full_text.split())

        processed_data = {
            "page_count": page_count,
            "word_count": word_count,
            "summary": full_text[:300]  # first 300 chars preview
        }

        # Update shared memory with processed PDF data
        shared_memory.update_entry(entry_id, {"pdf_processed": processed_data})

        print(f"[PDFAgent] Processed PDF ID: {entry_id}")
        print(f"  → Pages: {page_count}")
        print(f"  → Word count: {word_count}")
        print(f"  → Summary preview: {processed_data['summary']}")

