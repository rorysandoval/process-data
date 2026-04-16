import datetime
from typing import List, Dict, Any

class FileDataPersister:
    """Handles persistence of data to a file. Follows Single Responsibility Principle."""

    def __init__(self, filename: str = "data.txt"):
        self.filename = filename

    def save(self, records: List[Dict[str, Any]]) -> bool:
        """Save records to file with proper error handling."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(str(records))  # In production, prefer json.dumps for robustness
            print(f"Data successfully saved to {self.filename}.")
            return True
        except PermissionError:
            print(f"Error: Permission denied when writing to {self.filename}.")
            return False
        except OSError as e:
            print(f"Error saving data to {self.filename}: {e}")
            return False
        except Exception as e:  # Catch unexpected errors
            print(f"Unexpected error while saving data: {e}")
            return False


class DataStore:
    """Manages in-memory data records (add, show, persist). No globals."""

    def __init__(self, persister: FileDataPersister):
        self.records: List[Dict[str, Any]] = []
        self.persister = persister

    def add_record(self, value: str) -> None:
        """Add a new record with timestamp."""
        if not value or not value.strip():
            print("Error: Value cannot be empty.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = {
            'id': len(self.records) + 1,
            'val': value.strip(),
            'date': timestamp
        }
        self.records.append(new_record)
        print("Record added successfully.")

    def show_records(self) -> None:
        """Display all records in a clean format."""
        if not self.records:
            print("No records found.")
            return

        for record in self.records:
            print(f"Item: {record['id']} - {record['val']} at {record['date']}")

    def save_records(self) -> None:
        """Delegate saving to the persister."""
        self.persister.save(self.records)


class Authenticator:
    """Handles user authentication. Simple in-memory for demo (use secure methods in production)."""

    def __init__(self, username: str = "admin", password: str = "12345"):
        self.username = username
        self.password = password

    def check_credentials(self, username: str, password: str) -> bool:
        """Validate username and password."""
        return username == self.username and password == self.password


class CLIHandler:
    """Handles command-line interaction and main program flow."""

    def __init__(self, data_store: DataStore, authenticator: Authenticator):
        self.data_store = data_store
        self.authenticator = authenticator

    def run(self) -> None:
        """Main application loop."""
        username = input("User: ").strip()
        password = input("Pass: ").strip()

        if not self.authenticator.check_credentials(username, password):
            print("Wrong credentials!")
            return

        print("Welcome")

        while True:
            command = input("What to do? (add/show/save/exit): ").strip().lower()

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "add":
                value = input("Value: ").strip()
                self.data_store.add_record(value)
            elif command == "show":
                self.data_store.show_records()
            elif command == "save":
                self.data_store.save_records()
            else:
                print("Unknown command. Available commands: add, show, save, exit")


# ====================== Main Execution ======================

if __name__ == "__main__":
    # Dependency injection - no globals
    persister = FileDataPersister()
    data_store = DataStore(persister)
    authenticator = Authenticator()

    cli = CLIHandler(data_store, authenticator)
    cli.run()