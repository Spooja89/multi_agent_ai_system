# agents/json/json_agent.py

from pydantic import BaseModel, ValidationError, Field
from memory.memory_store import shared_memory


class TargetSchema(BaseModel):
    invoice_number: str = Field(..., alias="invoiceNum")
    amount: float
    vendor: str
    date: str

class JSONAgent:
    def __init__(self):
        pass

    def process(self, entry_id):
        data = shared_memory.retrieve(entry_id)
        if not data:
            print(f"[JSONAgent] No data found for entry ID: {entry_id}")
            return

        json_payload = data.get("raw_data")
        if not json_payload:
            print(f"[JSONAgent] No raw_data found for entry ID: {entry_id}")
            return

        try:
            validated = TargetSchema.parse_obj(json_payload)
            formatted = validated.dict(by_alias=True)
            anomalies = None
            print(f"[JSONAgent] Valid JSON processed for Entry ID: {entry_id}")
        except ValidationError as e:
            anomalies = e.errors()
            formatted = None
            print(f"[JSONAgent] Validation errors: {anomalies}")

        # Update shared memory
        shared_memory.update_entry(entry_id, {
            "json_processed": formatted,
            "anomalies": anomalies
        })

