# memory/__init__.py
import uuid

from .memory import SharedMemory

shared_memory = SharedMemory()

def init_db():
    shared_memory.create_table()

def add_entry(source, file_type, intent, metadata="{}"):
    id = str(uuid.uuid4())  # generate new unique id
    shared_memory.store(id, source, file_type, intent, metadata)
    return id
