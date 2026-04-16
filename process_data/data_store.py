# data_store.py
import datetime
import logging
from typing import List, Dict, Any

from .persister import FileDataPersister

logger = logging.getLogger(__name__)


class DataStore:
    """
    Manages in-memory collection of data records.
    """

    def __init__(self, persister: FileDataPersister):
        self.records: List[Dict[str, Any]] = []
        self.persister = persister
        self._next_id = 1
        logger.debug("DataStore initialized")

    def add_record(self, value: str) -> None:
        """Add a new record with validation."""
        if not value or not value.strip():
            logger.warning("Attempted to add empty value")
            print("Error: Value cannot be empty.")
            return

        if len(value) > 1000:
            logger.warning("Value too long (length: %d)", len(value))
            print("Error: Value is too long (maximum 1000 characters).")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record: Dict[str, Any] = {
            'id': self._next_id,
            'val': value.strip(),
            'date': timestamp
        }
        self.records.append(new_record)
        self._next_id += 1
        logger.info("Record added successfully (ID: %d)", new_record['id'])
        print("Record added successfully.")

    def show_records(self) -> None:
        """Display all stored records."""
        if not self.records:
            logger.info("show_records called - no records found")
            print("No records found.")
            return

        logger.info("Displaying %d records", len(self.records))
        for record in self.records:
            print(f"Item: {record['id']} - {record['val']} at {record['date']}")

    def save_records(self) -> None:
        """Delegate saving to the persister."""
        logger.info("save_records requested (%d records)", len(self.records))
        self.persister.save(self.records)