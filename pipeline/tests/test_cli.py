"""Tests for the command-line skeleton."""

import pytest

from plot_gallery import __version__
from plot_gallery.cli import COMMANDS, main


def test_help_lists_every_command(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(['--help'])

    assert exc_info.value.code == 0
    output = capsys.readouterr().out
    for name, _, _ in COMMANDS:
        assert name in output


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(['--version'])

    assert __version__ in capsys.readouterr().out


def test_no_command_prints_help_and_returns_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 2
    assert 'usage: gallery' in capsys.readouterr().out


def test_unimplemented_command_fails(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(['check', '--skip-notebooks']) == 1
    assert 'not implemented yet' in capsys.readouterr().err
