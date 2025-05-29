# dedupe_robot

A Python script to automatically sort files in your working directory into **unique** (`uni/`) and **duplicate** (`dup/`) folders based on filename, extension, and size rules.

## Features

- **Auto folder setup:** Creates `uni/` and `dup/` if they don’t exist.
- **Phase 1 (.ex4 & .ex5):** Groups by normalized name and exact file size.
- **Phase 2 (.zip & .rar):** Groups by normalized name only.
- **First vs. rest logic:** Moves the first (alphabetically) of each group to `uni/`, and duplicates to `dup/`. If a matching file already exists in `uni/`, all group members go to `dup/`.
- **Reporting:** Prints counts for each phase and pauses 5 seconds between them.
- **Idempotent:** Safe to rerun—already-sorted files are ignored.

## Requirements

- Python 3 (no external libraries needed)

## Usage

1. Place `dedupe_robot.py` in your target directory.
2. Open a terminal and `cd` to that directory.
3. Run:

   ```bash
   python dedupe_robot.py
   ```

4. Check `uni/` and `dup/` folders for sorted files.
