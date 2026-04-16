# Refactor Process for process_data.py

## 1. Plan

I refactored `process_data.py` to follow SOLID principles and remove global variables.
- Single Responsibility: separated responsibilities into distinct classes.
- Open/Closed: the persistence layer can be extended without modifying item logic.
- Liskov Substitution: persistence is encapsulated behind a dedicated class.
- Interface Segregation: command handling, authentication, and persistence are separate.
- Dependency Inversion: `ItemManager` depends on the abstract persistence behavior exposed by `DataPersistence`.

Global variables were removed. The script now builds objects in `main()` and passes them to collaborators.

## 2. Naming

I replaced the original cryptic names with descriptive names:
- `l` -> `self._items` inside `ItemManager` (items collection)
- `d` -> `credentials` (authentication credentials)
- `fn` -> `ItemManager.add_item`, `ItemManager.show_items`, `ItemManager.save_items` (clear command methods)

The renamed values describe actual domain concepts instead of vague single-letter names.

## 3. Modularization

The data persistence logic was extracted into a separate `DataPersistence` class.
- `DataPersistence.save` handles writing item data to disk.
- `ItemManager` delegates save actions to this class.
- This isolates file I/O so item management and persistence can evolve independently.

## 4. Error Handling

The file saving logic now includes explicit error handling:
- `DataPersistence.save` wraps file I/O in a `try`/`except OSError` block.
- If writing fails, it raises `RuntimeError` with a helpful message.
- `ItemManager.save_items` catches this `RuntimeError` and prints the error instead of crashing.

This covers failures such as permission errors, missing directories, or disk write issues.

## 5. Documentation

Docstrings were added for all classes and functions:
- `DataPersistence`
- `ItemManager`
- `Authenticator`
- `prompt_credentials`
- `prompt_command`
- `main`

The docstrings describe purpose, arguments, return types, and raised exceptions where relevant.
