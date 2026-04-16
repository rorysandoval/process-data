# Process Data Application by RORY SANDOVAL

A refactored Python command-line application for managing simple records with authentication and file persistence.

This project demonstrates best practices in Python development, including **SOLID principles**, clean architecture, proper error handling, and modular design.


## Process Data

A production-ready Python CLI tool for managing simple timestamped records with secure authentication and JSON persistence.

## Read LOG.md file 

As required there is a LOG.md file with the explanation of the work done.

## Features
- Secure bcrypt password hashing
- Structured logging with rotation (`app.log`)
- Command-line argument support via `argparse`
- Environment variable support
- Graceful error handling
- Installable as a console script (`process-data`)

## Installation

```bash
cd process_data
pip install -r requirements.txt
# or make it editable
pip install -e .
```

## Usage

```bash
# Interactive mode
process-data

# With overrides
process-data --username admin --password StrongPass123 -f mydata.json --log-level INFO

# Show version
process-data --version

# Help
process-data --help
```



## Security Recommendations

- Set APP_USERNAME and APP_PASSWORD as environment variables instead of passing via CLI.
- Never commit real passwords.
- Use a secrets manager in real deployments.



## Original code

```
process_data.py
```

## Refactoring Summary

The original `process_data.py` was refactored with the following improvements:

### 1. SOLID Principles & Removal of Global Variables
- Applied **Single Responsibility Principle (SRP)**: Each class now has one clear responsibility.
- Applied **Dependency Inversion Principle (DIP)**: High-level modules depend on abstractions rather than concrete implementations.
- Completely removed all global variables (`l`, `d`, etc.).
- Made the code more testable and maintainable through dependency injection.

### 2. Improved Naming
- `l` → `records` (list of data entries)
- `d` → `credentials` (moved into `Authenticator` class)
- `fn` → split into focused methods: `add_record()`, `show_records()`, `save_records()`
- All variables renamed for clarity (`u_in` → `username`, `v` → `value`, `cmd` → `command`, etc.)

### 3. Modularization
- Extracted data persistence logic into a dedicated `FileDataPersister` class.
- Split the monolithic file into multiple focused modules:
    - `persister.py` – File I/O operations
    - `data_store.py` – In-memory data management
    - `auth.py` – Authentication logic
    - `cli.py` – Command-line interface and user flow
    - `main.py` – Application entry point with dependency injection

### 4. Error Handling
- Added proper `try-except` blocks in file saving logic.
- Handles `PermissionError`, `OSError`, and unexpected exceptions gracefully.
- Added input validation (e.g., empty values are rejected).
- Prevents application crashes due to file I/O failures.

### Additional Improvements
- Removed dead/unused code (`calculate_something_else`).
- Used context managers (`with open...`) for file operations.
- Clean, readable output and better user experience.
- Professional project structure with clear separation of concerns.

## Project Structure

```
process_data/
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── process_data/
│   ├── __init__.py
│   ├── main.py
│   ├── cli.py
│   ├── data_store.py
│   ├── persister.py
│   └── auth.py
```




## Default Credentials

- Username: admin
- Password: 12345

Note: In a real application, never hardcode credentials. Use environment variables or a secure secrets manager.
Availabl

## Available Commands
Once logged in, you can use the following commands:

- **add**   – Add a new record with a value
- **show**  – Display all saved records
- **save**  – Save current records to data.txt
- **exit**  – Exit the application

## Future Enhancements (Suggestions)

- Add unit tests using pytest
- Support different storage backends (SQLite, JSON file, database)
- Use a CLI framework like typer or click

## Why This Refactoring Matters

- **Maintainable:** Easy to understand and modify
- **Testable:** Each class can be unit tested independently
- **Extensible:** New features can be added without breaking existing code
- **Professional:** Follows industry best practices and SOLID principles

---

## How it was requested:

( see details in the /docs/LOG.md file )

- **Plan:** How can I refactor "process_data.py" to follow SOLID principles and remove global variables?
- **Naming:** Suggest better names for variables 'l', 'd', and function 'fn' based on their usage.
- **Modularization:** Can you extract the data persistence logic into a separate class?
- **Error Handling:** Identify points of failure in the file saving logic and suggest
try-except blocks.

For each task, write the explanation of what you are doing. 
Then finally, split each feature in its own file. 


## Complete Code Generated (for reference) on first attempt.
```
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
```


## Security & Vulnerabilities Addressed

**Fixed in this version:**
- Hardcoded credentials → now loaded from environment variables (`APP_USERNAME`, `APP_PASSWORD`).
- Plain-text password storage → basic hashing added (recommend `bcrypt` for production).
- Insecure persistence format → switched to JSON.
- Potential path traversal → filename sanitized using `pathlib`.
- File handling → uses context managers and explicit UTF-8 encoding.

**Remaining recommendations for production:**

- Store secrets in a vault (e.g., HashiCorp Vault, AWS Secrets Manager).
- Add rate limiting on login attempts.
- Run with least-privilege user.

