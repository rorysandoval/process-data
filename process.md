# Code Smells and Refactor Plan

## Code smells identified

- Global mutable state with `l` and `d`.
- Single function `fn` with multiple responsibilities.
- Poor naming: `l`, `d`, `fn`.
- Hardcoded credentials stored in module-level dict.
- File persistence mixed with business logic.
- No use of `with` for file handling.
- No error handling around file operations.
- Dead / unused function `calculate_something_else`.
- No docstrings or structured module separation.

## Refactor plan

- Separate responsibilities into dedicated classes:
  - `Authenticator` for credential verification.
  - `ItemManager` for managing items in memory.
  - `DataPersistence` for saving items to disk.
- Keep `process_data.py` as the CLI orchestration module.
- Remove global variables.
- Store items in a class instance instead of a module-level list.
- Use JSON persistence instead of raw Python string dumps.

## Modularization

- `authenticator.py`
- `item_manager.py`
- `data_persistence.py`
- `process_data.py`

Each class is now in its own file.

## Error handling

- `DataPersistence.save` catches `OSError` and raises a `RuntimeError`.
- `process_data.py` catches `RuntimeError` during save and reports failure.
- This separates failure handling from persistence logic.

## Result

- Cleaner single responsibility design.
- Better testability.
- Easier future extension:
  - swap persistence backend
  - add new commands
  - replace authentication method
- Clearer naming and documentation.
