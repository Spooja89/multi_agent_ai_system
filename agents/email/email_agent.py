# agents/email/email_agent.py

import re
from memory.memory_store import shared_memory


class EmailAgent:
    def __init__(self):
        pass

    def detect_urgency(self, text):
        urgency_keywords = ["urgent", "asap", "immediately", "priority", "quickly"]
        for keyword in urgency_keywords:
            if keyword in text.lower():
                return "High"
        return "Normal"

    def extract_sender(self, text):
        # Simulate finding an email address
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        return match.group(0) if match else "unknown@domain.com"

    def process(self, entry_id):
        entry = shared_memory.retrieve(entry_id)
        if not entry:
            print(f"[EmailAgent] No entry found for ID: {entry_id}")
            return

        content = entry.get("content", "")
        sender = self.extract_sender(content)
        urgency = self.detect_urgency(content)
        intent = entry.get("intent", "Unknown")

        structured_data = {
            "sender": sender,
            "intent": intent,
            "urgency": urgency,
            "summary": content[:200]
        }

        shared_memory.update_entry(entry_id, {"email_processed": structured_data})

        print(f"[EmailAgent] Processed Email ID: {entry_id}")
        print(f"  → Sender: {sender}")
        print(f"  → Urgency: {urgency}")
        print(f"  → Intent: {intent}")
