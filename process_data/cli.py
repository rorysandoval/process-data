# cli.py
import logging
from .data_store import DataStore
from .auth import Authenticator

logger = logging.getLogger(__name__)


class CLIHandler:
    """
    Manages the command-line user interface and main application loop.
    """

    def __init__(self, data_store: DataStore, authenticator: Authenticator):
        self.data_store = data_store
        self.authenticator = authenticator
        logger.debug("CLIHandler initialized")

    def run(self) -> None:
        """Run the main interactive loop."""
        logger.info("Application started")
        print("=== Process Data Application ===")

        username = input("User: ").strip()
        password = input("Pass: ").strip()

        if not self.authenticator.check_credentials(username, password):
            print("Wrong credentials!")
            logger.info("Application exited due to failed authentication")
            return

        print("Welcome!")

        while True:
            command = input("\nWhat to do? (add/show/save/exit): ").strip().lower()

            if command == "exit":
                print("Goodbye!")
                logger.info("Application exited by user")
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
                logger.warning("Unknown command entered: %s", command)