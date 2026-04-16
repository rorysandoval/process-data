# main.py
import argparse
import logging
import os
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from .persister import FileDataPersister
from .data_store import DataStore
from .auth import Authenticator
from .cli import CLIHandler
from . import __version__


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging with rotation for production use."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger("process_data")
    root_logger.setLevel(numeric_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (user-friendly output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Rotating file handler (production best practice)
    log_file = Path("app.log")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    root_logger.info("Logging initialized at level %s (version: %s)", log_level, __version__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process Data - Production-ready CLI record manager",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Security note: Avoid passing --password in shared environments."
    )

    parser.add_argument(
        "-u", "--username",
        help="Username for authentication",
        default=os.getenv("APP_USERNAME", "admin")
    )

    parser.add_argument(
        "-p", "--password",
        help="Password for authentication (overrides APP_PASSWORD). "
             "WARNING: Visible in process list.",
        default=os.getenv("APP_PASSWORD", "12345")
    )

    parser.add_argument(
        "-f", "--file",
        help="Custom JSON filename for data storage",
        default="data.json"
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level",
        default="INFO"
    )

    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )

    return parser.parse_args()


def main() -> None:
    """Production-ready application entry point."""
    try:
        args = parse_arguments()

        setup_logging(args.log_level)
        logger = logging.getLogger("process_data")

        logger.info("Starting Process Data v%s", __version__)

        # Dependency injection
        persister = FileDataPersister(filename=args.file)
        data_store = DataStore(persister)
        authenticator = Authenticator(username=args.username, password=args.password)

        cli = CLIHandler(data_store, authenticator)
        cli.run()

        logger.info("Application shutdown gracefully")

    except Exception:
        logging.getLogger("process_data").exception("Unexpected fatal error")
        print("\nA critical error occurred. Check app.log for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()