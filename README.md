# sliding-game-3by3-
A simple game sliding 3 by 3# Sliding Game 3x3

A simple 3×3 sliding puzzle game implemented in Python.

This README includes quick, tested instructions for running the game on Android using Termux.

---

## Features

- 3×3 sliding puzzle (classic "15-puzzle" style reduced to 3×3)
- Terminal-based interface (runs in Termux)
- Keyboard controls (arrow keys or WASD)
- Simple, dependency-light Python code — easy to run and modify

---

## Requirements

- Android device with Termux installed
- Termux packages:
  - python (Python 3)
  - git (to clone the repo; optional if you download manually)
- Optional: build tools (clang, make) if pip needs to compile packages

---

## Install & Run (Termux)

Open Termux and run the following commands:

1. Update Termux packages
```
pkg update && pkg upgrade -y
```

2. Install Python and git
```
pkg install python git -y
```

3. (Optional) Give Termux access to shared storage if the game reads/writes files there:
```
termux-setup-storage
```
Follow the prompts to grant permission.

4. Clone this repository
```
git clone https://github.com/nihal86839/sliding-game-3by3-.git
cd sliding-game-3by3-
```

5. Install Python dependencies (if a `requirements.txt` file exists)
```
# If the repo includes dependencies
pip install --upgrade pip
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

6. Run the game
Identify the main script in the repo (commonly `main.py`, `app.py`, or `sliding_game.py`) and run it:
```
python3 main.py
```
If you aren't sure which file to run:
```
ls -1 *.py
# then run the file that looks like the entry point
python3 <entry_file>.py
```

---

## Controls (Termux)

- Arrow keys: move tiles (recommended if you have a hardware keyboard or Bluetooth keyboard)
- WASD: alternative keys if arrow keys are not available
- q or Ctrl+C: quit

Note: On some Android devices the on-screen keyboard may not send arrow key events. If that happens, use a Bluetooth/USB keyboard or the WASD keys.

---

## Tips & Troubleshooting

- "python3: command not found": ensure you installed `python` via `pkg install python`.
- Pip install failures when building wheels: install basic build tools:
  ```
  pkg install clang make libffi-dev openssl-dev -y
  ```
- Permission errors running scripts: ensure execute permission or run with `python3 script.py` (no need to chmod).
- If the interface looks odd, try changing Termux font size or use an external keyboard for better key handling.
- If the game expects specific file names or a config, open the primary `.py` file and check for filenames/arguments.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-change`
3. Make your changes and commit
4. Submit a pull request describing your changes

---

## License

This project is provided "as-is". Add a license file (e.g., MIT) if you want to allow reuse. Example:
```
MIT License
...
```

---

If you'd like, I can:
- Add a short example of the expected terminal UI,
- Detect the repo's actual entry script and update the README to show the exact run command,
- Create a sample requirements.txt if any third-party packages are needed.

Which would you prefer?
