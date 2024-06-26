import os
import pexpect
from pathlib import Path
from textwrap import dedent


def test_history_not_log_auth(cli):
    cli.sendline("AUTH 123")
    cli.expect(["Client sent AUTH, but no password is set", "127.0.0.1"])
    cli.sendline("set foo bar")
    cli.expect("OK")

    with open(os.path.expanduser("~/.dice_history")) as history_file:
        content = history_file.read()

    assert "set foo bar" in content
    assert "AUTH" not in content


def test_history_create_and_writing_with_config():
    config_content = dedent(
        """
        [main]
        history_location = /tmp/dice_history.txt
        """
    )
    with open("/tmp/dicerc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn("dice -n 15 --dicerc /tmp/dicerc", timeout=2)
    cli.expect("127.0.0.1")
    cli.sendline("set hello world")
    cli.expect("OK")
    cli.close()

    log = Path("/tmp/dice_history.txt")
    assert log.exists()

    with open(log) as logfile:
        content = logfile.read()

    assert "set hello world" in content
