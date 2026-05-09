# SenType

SenType is a simple terminal typing practice game for sentence and word drills.

## Features

- Sentence mode by default
- Easy, medium, and hard sentence pools
- Optional word mode
- Fixed-count or timed sessions
- Per-sentence mismatch indicators
- WPM, accuracy, and high-score tracking

## Usage

```sh
python3 game.py
python3 game.py -s 10 -d easy
python3 game.py -s 10 -d hard
python3 game.py -t 60 -d medium
python3 game.py --mode words -w 20
python3 game.py -f /path/to/file.txt
```

Installed packages provide the `sentype` command:

```sh
sentype
sentype --version
sentype -s 10 -d hard
```

High scores are stored in `~/.sentype_scores.json`.

## Windows Build

The recommended Windows release asset is a Nuitka one-file executable. Build it
on Windows with Python 3.12:

```powershell
.\build-windows.ps1
```

## License

MIT
