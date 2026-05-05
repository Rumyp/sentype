#!/usr/bin/env python3
"""
DonkeyType — terminal typing game (sentence mode) with difficulty levels
Usage examples:
  python3 game.py                 # sentence mode (default), 5 sentences, medium difficulty
  python3 game.py -s 10 -d easy    # 10 easy sentences
  python3 game.py -t 60 -d hard    # timed mode (60s) using hard sentences
  python3 game.py --mode words -w 20  # legacy word mode

New: --difficulty / -d with easy, medium, hard pools.
"""

import argparse
import random
import time
import sys
import os
import json

SCORES_PATH = os.path.expanduser("~/.donkeytype_scores.json")


def load_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def countdown(n=3):
    for i in range(n, 0, -1):
        print(f"Starting in {i}...", end="\r", flush=True)
        time.sleep(1)
    print(" "*40, end="\r")


def show_diff(target, typed):
    # Print target and typed and an indicator line showing mismatches
    print('\nTarget: ' + target)
    print('Typed : ' + typed)
    # build indicator
    indicator = []
    for i in range(max(len(target), len(typed))):
        a = typed[i] if i < len(typed) else None
        b = target[i] if i < len(target) else None
        if a == b:
            indicator.append(' ')
        else:
            indicator.append('^')
    print('        ' + ''.join(indicator))


def run_sentence_mode(sentences, count, timed):
    chosen = random.sample(sentences, min(count, len(sentences))) if count and not timed else None
    total_chars = 0
    correct_chars = 0
    sentences_done = 0
    start = None

    print('\nSentence mode. Press Ctrl+C to stop early.')
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
                typed = input('Type: ')
                sentences_done += 1
                total_chars += len(typed)
                for a, b in zip(typed, target):
                    if a == b:
                        correct_chars += 1
                show_diff(target, typed)
        else:
            for idx, target in enumerate(chosen, 1):
                print(f"\nSentence {idx}/{len(chosen)}: {target}")
                typed = input('Type: ')
                sentences_done += 1
                total_chars += len(typed)
                for a, b in zip(typed, target):
                    if a == b:
                        correct_chars += 1
                show_diff(target, typed)
    except KeyboardInterrupt:
        print('\nInterrupted.')

    end = time.perf_counter()
    elapsed = end - start if start else 0.0
    return elapsed, total_chars, correct_chars, sentences_done


def run_word_mode(words, n, timed):
    chosen = random.sample(words, min(n, len(words))) if n and not timed else None
    total_chars = 0
    correct_chars = 0
    words_done = 0
    start = None

    print('\nWord mode. Press Ctrl+C to stop early.')
    countdown(3)
    start = time.perf_counter()

    try:
        if timed:
            while True:
                now = time.perf_counter()
                if now - start >= timed:
                    break
                w = random.choice(words)
                print(f"\nTarget: {w}")
                typed = input('Type: ')
                words_done += 1
                total_chars += len(typed)
                for a, b in zip(typed, w):
                    if a == b:
                        correct_chars += 1
        else:
            for idx, w in enumerate(chosen, 1):
                print(f"\nWord {idx}/{len(chosen)}: {w}")
                typed = input('Type: ')
                words_done += 1
                total_chars += len(typed)
                for a, b in zip(typed, w):
                    if a == b:
                        correct_chars += 1
    except KeyboardInterrupt:
        print('\nInterrupted.')

    end = time.perf_counter()
    elapsed = end - start if start else 0.0
    return elapsed, total_chars, correct_chars, words_done


def print_stats(elapsed, total_chars, correct_chars, items_done):
    minutes = elapsed / 60 if elapsed > 0 else 1e-9
    wpm = (correct_chars / 5) / minutes
    accuracy = (correct_chars / total_chars * 100) if total_chars > 0 else 0.0
    print('\n--- Results ---')
    print(f"Time: {elapsed:.2f}s")
    print(f"WPM: {wpm:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Items typed: {items_done}")
    return wpm


def load_scores():
    try:
        with open(SCORES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_scores(scores):
    try:
        with open(SCORES_PATH, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2)
    except Exception:
        pass


def update_high_scores(mode_key, wpm):
    scores = load_scores()
    prev = scores.get(mode_key, 0)
    if wpm > prev:
        scores[mode_key] = wpm
        save_scores(scores)
        print(f"New high score for {mode_key}: {wpm:.2f} WPM (previous {prev:.2f})")
    else:
        print(f"High score for {mode_key}: {prev:.2f} WPM")


def main():
    parser = argparse.ArgumentParser(description="DonkeyType — typing game (sentence mode)")
    parser.add_argument('--mode', choices=['sentences', 'words'], default='sentences', help='Mode: sentences (default) or words')
    parser.add_argument('-s', '--sentences', type=int, default=5, help='Number of sentences for sentence mode (default 5)')
    parser.add_argument('-w', '--words', type=int, default=10, help='Number of words for word mode (default 10)')
    parser.add_argument('-t', '--timed', type=int, default=0, help='Timed mode in seconds (e.g., 60). If set, runs timed session')
    parser.add_argument('-f', '--file', default=None, help='Path to sentence/word list file (defaults to sentences_<difficulty>.txt for sentences mode, words.txt for words mode)')
    parser.add_argument('-d', '--difficulty', choices=['easy', 'medium', 'hard'], default='medium', help='Difficulty for sentence mode (easy, medium, hard). Default: medium')
    args = parser.parse_args()

    base_dir = os.path.dirname(__file__)
    if args.file:
        path = args.file if os.path.isabs(args.file) else os.path.join(base_dir, args.file)
    else:
        if args.mode == 'sentences':
            default_file = f'sentences_{args.difficulty}.txt'
        else:
            default_file = 'words.txt'
        path = os.path.join(base_dir, default_file)

    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    lines = load_lines(path)
    if args.mode == 'sentences':
        elapsed, total_chars, correct_chars, done = run_sentence_mode(lines, args.sentences, args.timed)
    else:
        elapsed, total_chars, correct_chars, done = run_word_mode(lines, args.words, args.timed)

    wpm = print_stats(elapsed, total_chars, correct_chars, done)
    # include difficulty in score key for sentences
    if args.mode == 'sentences':
        mode_key = f"sentences:{args.difficulty}: {'timed' if args.timed>0 else 'count'}:{args.timed if args.timed>0 else args.sentences}"
    else:
        mode_key = f"words: {'timed' if args.timed>0 else 'count'}:{args.timed if args.timed>0 else args.words}"
    update_high_scores(mode_key, wpm)

if __name__ == '__main__':
    main()
