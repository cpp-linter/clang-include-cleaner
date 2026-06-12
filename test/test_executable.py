import os
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def ensure_include_cleaner_from_wheel(monkeypatch):
    """test the installed clang_include_cleaner package, not the local one"""
    this_dir = Path(__file__).resolve().absolute().parent
    for pd in (this_dir, this_dir / ".."):
        try:
            new_path = sys.path.remove(pd)
            monkeypatch.setattr(sys, "path", new_path)
        except ValueError:
            pass
    monkeypatch.delitem(sys.modules, "clang_include_cleaner", raising=False)


def test_executable_file(capsys):
    import clang_include_cleaner

    clang_include_cleaner._get_executable.cache_clear()
    exe = clang_include_cleaner.get_executable("clang-include-cleaner")
    assert os.path.exists(exe)
    assert os.access(exe, os.X_OK)
    assert capsys.readouterr().out == ""


def _test_help():
    import clang_include_cleaner

    assert (
        clang_include_cleaner._run(
            "clang-include-cleaner",
            "--help",
        ) == 0
    )


def test_verbose_output(capsys, monkeypatch):
    import clang_include_cleaner
    monkeypatch.setenv("CLANG_INCLUDE_CLEANER_WHEEL_VERBOSE", "1")
    # need to clear cache to make sure the function is run again
    clang_include_cleaner._get_executable.cache_clear()
    clang_include_cleaner.get_executable("clang-include-cleaner")
    assert capsys.readouterr().out


def test_help():
    _test_help()
