import pytest

def test_cli_help_runs():
    from assistant.cli import main
    try:
        main(["--help"])
    except SystemExit as e:
        assert e.code == 0
