import datetime
import json
from typing import Any, Dict, List, Tuple


class DataPersistence:
    """Handles persistence of item data to a file."""

    def __init__(self, file_path: str = "data.txt") -> None:
        self.file_path = file_path

    def save(self, items: List[Dict[str, Any]]) -> None:
        """Save the item list to the configured file path.

        Args:
            items: The list of item dictionaries to persist.

        Raises:
            RuntimeError: If the file cannot be written.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(items, file, indent=2)
        except OSError as error:
            raise RuntimeError(
                f"Unable to save data to '{self.file_path}': {error}"
            ) from error


class ItemManager:
    """Manages item collection and delegates persistence."""

    def __init__(self, persistence: DataPersistence) -> None:
        self._items: List[Dict[str, Any]] = []
        self._persistence = persistence

    def add_item(self, value: str) -> None:
        """Add a new item with metadata to the in-memory collection."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item_id = len(self._items) + 1
        self._items.append({
            "id": item_id,
            "value": value,
            "created_at": timestamp,
        })
        print("Added.")

    def show_items(self) -> None:
        """Print all stored items to the console."""
        if not self._items:
            print("No items to show.")
            return

        for item in self._items:
            print(
                f"Item: {item['id']} - {item['value']} at {item['created_at']}"
            )

    def save_items(self) -> None:
        """Persist current items and handle save errors."""
        try:
            self._persistence.save(self._items)
            print("Saved.")
        except RuntimeError as error:
            print(error)


class Authenticator:
    """Validates user credentials against a stored credential set."""

    def __init__(self, credentials: Dict[str, str]) -> None:
        self._credentials = credentials

    def validate(self, username: str, password: str) -> bool:
        """Return True if provided credentials match the stored values."""
        return (
            username == self._credentials.get("username")
            and password == self._credentials.get("password")
        )


def prompt_credentials() -> Tuple[str, str]:
    """Request username and password from the user."""
    username = input("User: ")
    password = input("Pass: ")
    return username, password


def prompt_command() -> str:
    """Request the next command from the user."""
    return input("What to do? (add/show/save/exit): ").strip().lower()


def main() -> None:
    """Run the command loop for the process data script."""
    credentials = {"username": "admin", "password": "12345"}
    authenticator = Authenticator(credentials)
    persistence = DataPersistence()
    item_manager = ItemManager(persistence)

    username, password = prompt_credentials()
    if not authenticator.validate(username, password):
        print("Wrong!")
        return

    print("Welcome")
    while True:
        command = prompt_command()

        if command == "exit":
            break
        if command == "add":
            value = input("Value: ")
            item_manager.add_item(value)
        elif command == "show":
            item_manager.show_items()
        elif command == "save":
            item_manager.save_items()
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
