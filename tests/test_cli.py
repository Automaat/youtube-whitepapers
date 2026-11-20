"""Tests for odczyt.cli argument handling."""

import pytest

from odczyt.cli import episode_numbers


@pytest.mark.parametrize(
    ("spec", "expected"),
    [("73", [73]), ("64-66", [64, 65, 66]), ("64,70-71", [64, 70, 71]), (" 5 , 7 ", [5, 7])],
)
def test_episode_numbers(spec, expected):
    assert episode_numbers(spec) == expected
