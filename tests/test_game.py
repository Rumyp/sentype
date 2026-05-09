import argparse
from pathlib import Path

import game


def test_score_attempt_counts_missing_characters():
    assert game.score_attempt("hello", "he") == (2, 5)


def test_score_attempt_counts_extra_characters():
    assert game.score_attempt("hi", "hike") == (2, 4)


def test_positive_int_rejects_zero():
    try:
        game.positive_int("0")
    except argparse.ArgumentTypeError:
        return
    raise AssertionError("positive_int accepted zero")


def test_resolve_default_sentence_file(monkeypatch, tmp_path):
    monkeypatch.setattr(game, "resource_dir", lambda: Path(tmp_path))
    args = argparse.Namespace(file=None, mode="sentences", difficulty="hard")
    assert game.resolve_input_file(args) == Path(tmp_path) / "sentences_hard.txt"
