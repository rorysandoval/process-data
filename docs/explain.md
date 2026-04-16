# process_data.py

`process_data.py` is a simple Python CLI script that:

- imports `datetime`
- defines global state:
  - `l` as a list for stored items
  - `d` as a dictionary with hardcoded credentials `{"u": "admin", "p": "12345"}`

## Functions

- `fn(a, b)`
  - performs multiple actions based on the command `a`
  - if `a == "add"`:
    - creates a timestamp
    - appends a new item to `l` with `id`, `val`, and `date`
    - prints `Added.`
  - if `a == "show"`:
    - iterates over `l`
    - prints each stored item
  - if `a == "save"`:
    - opens `data.txt` for writing
    - writes the string representation of `l`
    - closes the file
    - prints `Saved.`

- `check(u, p)`
  - compares the provided username and password against the hardcoded values in `d`
  - returns `True` only if both match

- `calculate_something_else(x)`
  - a dead / unused helper function
  - sums integers from `0` to `x - 1`
  - never called by the script

## Main execution flow

- prompts the user for `User:` and `Pass:`
- if `check(u_in, p_in)` returns `True`:
  - prints `Welcome`
  - enters a loop asking for `What to do? (add/show/save/exit):`
  - if command is `add`:
    - prompts for `Value:`
    - calls `fn("add", v)`
  - if command is `exit`:
    - breaks the loop
  - otherwise:
    - calls `fn(cmd, None)` for `show` or `save`
- if authentication fails:
  - prints `Wrong!`

## Issues

- uses global mutable state in `l`
- stores credentials insecurely in source code
- `fn` is cryptic and handles multiple responsibilities
- lacks input validation
- writes files without a `with` context manager
- saves `l` as a raw Python string instead of a structured format
- contains unused dead code

---

## What the Code Does (High-Level Overview)

This script is a **very basic interactive command-line application** that acts as a simple in-memory "database" with insecure login protection.

**Features:**
- Username and password authentication (hardcoded)
- After successful login, the user can:
  - **Add** an item with a value (automatically gets an ID and timestamp)
  - **Show** all added items
  - **Save** the current list to a file named `data.txt`
  - **Exit** the program

Data is stored temporarily in memory using a global list and can be written to a text file.

