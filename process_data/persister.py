# persister.py
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class FileDataPersister:
    """
    Handles persistence of records to a JSON file using safe pathlib operations.
    """

    def __init__(self, filename: str = "data.json", base_dir: Path | None = None):
        """
        Initialize the persister with a safe file path.

        Args:
            filename: Desired filename (will be sanitized).
            base_dir: Base directory where files are allowed (defaults to cwd).

        Raises:
            ValueError: If the resulting path is outside the allowed base directory.
        """
        self.base_dir = (Path(base_dir) if base_dir else Path.cwd()).resolve()
        safe_name = Path(filename).name
        if not safe_name.lower().endswith(".json"):
            safe_name = "data.json"

        self.file_path = (self.base_dir / safe_name).resolve()

        if not self.file_path.is_relative_to(self.base_dir):
            raise ValueError("Invalid file path: outside allowed base directory.")

        logger.info("FileDataPersister initialized with path: %s", self.file_path.name)

    def save(self, records: List[Dict[str, Any]]) -> bool:
        """
        Save records to JSON file.

        Returns:
            bool: True if save succeeded, False otherwise.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            logger.info("Data successfully saved to %s (%d records)", 
                       self.file_path.name, len(records))
            return True
        except PermissionError:
            logger.warning("Permission denied when writing to %s", self.file_path.name)
            print("Error: Permission denied when writing to data file.")
            return False
        except OSError as e:
            logger.error("OSError while saving data: %s", e)
            print(f"Error saving data: {e}")
            return False
        except TypeError as e:
            logger.error("Data serialization error: %s", e)
            print(f"Data serialization error: {e}")
            return False
        except Exception:
            logger.exception("Unexpected error while saving data")
            print("Unexpected error while saving data.")
            return False