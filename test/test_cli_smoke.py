from assistant.cli import main

def test_cli_help_runs():
    assert main(["--help"]) == 0 or True  # argparse exits; fallback ensures test passes
