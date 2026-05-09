#!/usr/bin/env python3
import argparse
import json
import random
import sys
import time
from pathlib import Path

APP_NAME = "SenType"
VERSION = "0.2.1"
SCORES_PATH = Path.home() / ".sentype_scores.json"

BANNER = r"""
   _____          ______
  / ___/___  ____/_  __/_  ______  ___
  \__ \/ _ \/ __ \/ / / / / / __ \/ _ \
 ___/ /  __/ / / / / / /_/ / /_/ /  __/
/____/\___/_/ /_/_/  \__, / .___/\___/
                    /____/_/
          Terminal Typing Practice Game
"""


def resource_dir():
    """Return the directory containing bundled word and sentence lists."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    local_dir = Path(__file__).resolve().parent
    if (local_dir / "words.txt").exists():
        return local_dir
    installed_dir = Path(sys.prefix) / "share" / "sentype"
    if (installed_dir / "words.txt").exists():
        return installed_dir
    return local_dir


def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return number


def non_negative_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be 0 or greater")
    return number


def countdown(n=3):
    try:
        for i in range(n, 0, -1):
            print(f"Starting in {i}...", end="\r", flush=True)
            time.sleep(1)
        print(" " * 40, end="\r")
    except KeyboardInterrupt:
        print("\nInterrupted during countdown.")
        sys.exit(0)


def score_attempt(target, typed):
    correct = sum(1 for typed_char, target_char in zip(typed, target) if typed_char == target_char)
    possible = max(len(target), len(typed))
    return correct, possible


def show_diff(target, typed):
    print("\nTarget: " + target)
    print("Typed : " + typed)
    indicator = []
    for i in range(max(len(target), len(typed))):
        typed_char = typed[i] if i < len(typed) else None
        target_char = target[i] if i < len(target) else None
        indicator.append(" " if typed_char == target_char else "^")
    print("        " + "".join(indicator))


def record_attempt(target, typed):
    correct, possible = score_attempt(target, typed)
    show_diff(target, typed)
    return correct, possible


def run_sentence_mode(sentences, count, timed):
    chosen = random.sample(sentences, min(count, len(sentences))) if count and not timed else None
    possible_chars = 0
    correct_chars = 0
    sentences_done = 0
    start = None

    print("\nSentence mode. Press Ctrl+C to stop early.")
    countdown(3)
    start = time.perf_counter()

    try:
        if timed:
            while True:
                now = time.perf_counter()
                if now - start >= timed:
                    break
                target = random.choice(sentences)
                print(f"\nSentence: {target}")
                typed = input("Type: ")
                sentences_done += 1
                correct, possible = record_attempt(target, typed)
                correct_chars += correct
                possible_chars += possible
        else:
            for idx, target in enumerate(chosen, 1):
                print(f"\nSentence {idx}/{len(chosen)}: {target}")
                typed = input("Type: ")
                sentences_done += 1
                correct, possible = record_attempt(target, typed)
                correct_chars += correct
                possible_chars += possible
    except KeyboardInterrupt:
        print("\nInterrupted.")

    elapsed = time.perf_counter() - start if start else 0.0
    return elapsed, possible_chars, correct_chars, sentences_done


def run_word_mode(words, n, timed):
    chosen = random.sample(words, min(n, len(words))) if n and not timed else None
    possible_chars = 0
    correct_chars = 0
    words_done = 0
    start = None

    print("\nWord mode. Press Ctrl+C to stop early.")
    countdown(3)
    start = time.perf_counter()

    try:
        if timed:
            while True:
                now = time.perf_counter()
                if now - start >= timed:
                    break
                word = random.choice(words)
                print(f"\nTarget: {word}")
                typed = input("Type: ")
                words_done += 1
                correct, possible = score_attempt(word, typed)
                correct_chars += correct
                possible_chars += possible
        else:
            for idx, word in enumerate(chosen, 1):
                print(f"\nWord {idx}/{len(chosen)}: {word}")
                typed = input("Type: ")
                words_done += 1
                correct, possible = score_attempt(word, typed)
                correct_chars += correct
                possible_chars += possible
    except KeyboardInterrupt:
        print("\nInterrupted.")

    elapsed = time.perf_counter() - start if start else 0.0
    return elapsed, possible_chars, correct_chars, words_done


def print_stats(elapsed, possible_chars, correct_chars, items_done):
    minutes = elapsed / 60 if elapsed > 0 else 1e-9
    wpm = (correct_chars / 5) / minutes
    accuracy = (correct_chars / possible_chars * 100) if possible_chars > 0 else 0.0
    print("\n--- Results ---")
    print(f"Time: {elapsed:.2f}s")
    print(f"WPM: {wpm:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Items typed: {items_done}")
    return wpm


def load_scores():
    try:
        with open(SCORES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_scores(scores):
    try:
        with open(SCORES_PATH, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError as exc:
        print(f"Could not save high scores to {SCORES_PATH}: {exc}", file=sys.stderr)


def update_high_scores(mode_key, wpm):
    scores = load_scores()
    prev = scores.get(mode_key, 0)
    if wpm > prev:
        scores[mode_key] = wpm
        save_scores(scores)
        print(f"New high score for {mode_key}: {wpm:.2f} WPM (previous {prev:.2f})")
    else:
        print(f"High score for {mode_key}: {prev:.2f} WPM")


def build_parser():
    parser = argparse.ArgumentParser(description="SenType - terminal typing practice", prog="sentype")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--mode", choices=["sentences", "words"], default="sentences", help="Mode: sentences (default) or words")
    parser.add_argument("-s", "--sentences", type=positive_int, default=5, help="Number of sentences for sentence mode (default 5)")
    parser.add_argument("-w", "--words", type=positive_int, default=10, help="Number of words for word mode (default 10)")
    parser.add_argument("-t", "--timed", type=non_negative_int, default=0, help="Timed mode in seconds (e.g. 60); 0 disables timed mode")
    parser.add_argument("-f", "--file", default=None, help="Path to sentence/word list file")
    parser.add_argument("-d", "--difficulty", choices=["easy", "medium", "hard"], default="medium", help="Difficulty for sentence mode")
    return parser


def resolve_input_file(args):
    base_dir = resource_dir()
    if args.file:
        file_path = Path(args.file)
        return file_path if file_path.is_absolute() else base_dir / file_path
    if args.mode == "sentences":
        return base_dir / f"sentences_{args.difficulty}.txt"
    return base_dir / "words.txt"


def main(argv=None):
    print(BANNER)
    parser = build_parser()
    args = parser.parse_args(argv)

    path = resolve_input_file(args)
    if not path.exists():
        print(f"File not found: {path}")
        return 1

    lines = load_lines(path)
    if not lines:
        print(f"No usable lines found in {path}")
        return 1

    if args.mode == "sentences":
        elapsed, possible_chars, correct_chars, done = run_sentence_mode(lines, args.sentences, args.timed)
        mode_key = f"sentences:{args.difficulty}:{'timed' if args.timed > 0 else 'count'}:{args.timed if args.timed > 0 else args.sentences}"
    else:
        elapsed, possible_chars, correct_chars, done = run_word_mode(lines, args.words, args.timed)
        mode_key = f"words:{'timed' if args.timed > 0 else 'count'}:{args.timed if args.timed > 0 else args.words}"

    wpm = print_stats(elapsed, possible_chars, correct_chars, done)
    update_high_scores(mode_key, wpm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
