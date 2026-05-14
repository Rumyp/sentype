# Sentype


![sentype](https://img.shields.io/badge/sentype-terminal%20typing%20game-000000?style=for-the-badge&logo=windowsterminal&logoColor=00ff00)
![python](https://img.shields.io/badge/python-3.11+-000000?style=for-the-badge&logo=python&logoColor=00ff00)
![license](https://img.shields.io/github/license/rumyp/sentype?style=for-the-badge&color=000000&logoColor=00ff00)
![stars](https://img.shields.io/github/stars/rumyp/sentype?style=for-the-badge&color=000000&logoColor=00ff00)
![linux](https://img.shields.io/badge/Linux-AUR-000000?style=for-the-badge&logo=linux&logoColor=00ff00)
![windows](https://img.shields.io/badge/Windows-winget-000000?style=for-the-badge&logo=windows&logoColor=00ff00)
<img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=22&pause=1000&color=00FF00&center=true&vCenter=true&width=600&lines=terminal+typing+game...;yay+-S+sentype;winget+install+sentype" >


SenType is a simple terminal typing practice game for sentence and word drills.

## Features

- Sentence mode by default
- Easy, medium, and hard sentence pools
- Optional word mode
- Fixed-count or timed sessions
- Per-sentence mismatch indicators
- WPM, accuracy, and high-score tracking


# installation 

## windows
```sh
winget install sentype
```
or
```sh
winget install --id=Rumyp.Sentype -e
```
## Arch linux
```sh
yay -S sentype
```
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

## License

MIT
