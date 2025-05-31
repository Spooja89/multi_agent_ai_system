import sqlite3
import uuid
import datetime
import json

DB_PATH = "database/memory.db"

class SharedMemory:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS memory (
            id TEXT PRIMARY KEY,
            source TEXT,
            format TEXT,
            intent TEXT,
            timestamp TEXT,
            metadata TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def store(self, id=None, source=None, file_format=None, intent=None, metadata="{}"):
        if id is None:
            id = str(uuid.uuid4())  # generate unique id if none provided
        timestamp = datetime.datetime.now().isoformat()
        query = """
        INSERT INTO memory (id, source, format, intent, timestamp, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (id, source, file_format, intent, timestamp, metadata))
        self.conn.commit()
        return id

    def retrieve(self, entry_id):
        query = "SELECT * FROM memory WHERE id = ?"
        cur = self.conn.execute(query, (entry_id,))
        row = cur.fetchone()
        if row:
            return {
                "id": row[0],
                "source": row[1],
                "format": row[2],
                "intent": row[3],
                "timestamp": row[4],
                "metadata": row[5],
            }
        return None

    def update_entry(self, entry_id, updated_metadata):
        """
        Merge updated_metadata with existing metadata and update the record.
        """
        existing = self.retrieve(entry_id)
        if not existing:
            raise ValueError(f"No memory entry found with ID: {entry_id}")
        
        try:
            current_metadata = json.loads(existing["metadata"])
        except json.JSONDecodeError:
            current_metadata = {}

        current_metadata.update(updated_metadata)
        new_metadata = json.dumps(current_metadata)

        query = "UPDATE memory SET metadata = ? WHERE id = ?"
        self.conn.execute(query, (new_metadata, entry_id))
        self.conn.commit()
