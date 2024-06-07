import pexpect
from textwrap import dedent
from pathlib import Path


def test_log_location_config():
    config_content = dedent(
        """
        [main]
        log_location = /tmp/dice1.log
        """
    )
    with open("/tmp/dicerc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn("dice -n 15 --dicerc /tmp/dicerc", timeout=1)
    cli.expect("127.0.0.1")
    cli.close()

    log = Path("/tmp/dice1.log")
    assert log.exists()
    with open(log) as logfile:
        content = logfile.read()

    assert len(content) > 100


def test_load_prompt_from_config(dice_client, clean_redis):
    config_content = dedent(
        """
        [main]
        prompt = {host}abc{port}xx{db}
        """
    )
    with open("/tmp/dicerc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn("dice -n 15 --dicerc /tmp/dicerc", timeout=1)
    cli.expect("dice")
    cli.expect("127.0.0.1abc6379xx15")
    cli.close()


def test_prompt_cli_overwrite_config(dice_client, clean_redis):
    config_content = dedent(
        """
        [main]
        prompt = {host}abc{port}xx{db}
        """
    )
    with open("/tmp/dicerc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn(
        "dice -n 15 --dicerc /tmp/dicerc --prompt='{db}-12345'", timeout=1
    )
    cli.expect("dice")
    cli.expect("15-12345")
    cli.close()
