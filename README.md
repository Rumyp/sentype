DonkeyType — enhanced

Now defaults to sentence mode (better for realistic typing practice).

Usage:
  python3 game.py                 # sentence mode, 5 sentences (medium)
  python3 game.py -s 10 -d easy   # 10 easy sentences
  python3 game.py -s 10 -d hard   # 10 hard sentences
  python3 game.py -t 60 -d medium # timed mode (60 seconds)
  python3 game.py --mode words -w 20  # legacy word mode
  python3 game.py -f /path/to/file.txt  # use custom sentence/word list

New features:
- Sentence pools by difficulty: sentences_easy.txt, sentences_medium.txt, sentences_hard.txt
- Difficulty flag (-d, --difficulty)
- Per-sentence feedback and mismatch indicator
- 3-second countdown before starting
- Timed or fixed-count sessions
- High scores stored in ~/.donkeytype_scores.json

Notes:
- Sentences files are in the game folder. Each file contains one sentence per line.
- Use -f to point at a custom file if desired.
