""" This module describes an example of a Pikcio contrat.
Version: 0.1
Author: Pikcio
"""
_RATE_1 = 0.4  # Internal rate. Not saved
_RATE_2 = 0.2  # Internal rate. Not saved
last_rate = None  # last given rate. Updated after each call


def _get_previous_rate():  # Internal helper function
    return last_rate or 0.0


def compute_rate(amount):  # endpoint 1
    # type: (float) -> float
    global last_rate
    last_rate = _RATE_1 if amount < 200 else _RATE_2
    return last_rate


def reset_last_rate():  # endpoint 2
    # type: () -> None
    global last_rate
    last_rate = None
