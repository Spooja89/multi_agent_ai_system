import json
import os
import pdfplumber
import uuid
from memory.memory_store import shared_memory


class ClassifierAgent:
    def __init__(self):
        self.supported_formats = ['pdf', 'json', 'txt']

    def classify_format(self, filepath):
        ext = os.path.splitext(filepath)[-1].lower()
        if ext.endswith(".pdf"):
            return "PDF"
        elif ext.endswith(".json"):
            return "JSON"
        elif ext.endswith(".txt"):
            return "Email"
        else:
            return "Unknown"

    def classify_intent(self, text):
        text = text.lower()
        if "invoice" in text:
            return "Invoice"
        elif "rfq" in text or "quotation" in text:
            return "RFQ"
        elif "complaint" in text:
            return "Complaint"
        elif "regulation" in text:
            return "Regulation"
        else:
            return "General"

    def extract_text(self, filepath, filetype):
        if filetype == "PDF":
            with pdfplumber.open(filepath) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif filetype == "JSON":
            with open(filepath, 'r') as f:
                return json.dumps(json.load(f))
        elif filetype == "Email":
            with open(filepath, 'r') as f:
                return f.read()
        else:
            return ""

    def process(self, filepath):
        file_format = self.classify_format(filepath)
        raw_text = self.extract_text(filepath, file_format)
        intent = self.classify_intent(raw_text)
        entry_id = str(uuid.uuid4())

        # Store metadata differently if it's JSON (save raw_data)
        if file_format == "JSON":
            with open(filepath, "r") as f:
                raw_data = f.read()
            shared_memory.store(
                id=entry_id,
                source=filepath,
                file_format=file_format,
                intent=intent,
                metadata=json.dumps({"raw_data": raw_data})
            )
        else:
            shared_memory.store(
                id=entry_id,
                source=filepath,
                file_format=file_format,
                intent=intent,
                metadata="{}"
            )

        print(f"[ClassifierAgent] File: {filepath}")
        print(f"  → Format: {file_format}")
        print(f"  → Intent: {intent}")
        print(f"  → Entry ID in memory: {entry_id}")

        return entry_id, file_format
