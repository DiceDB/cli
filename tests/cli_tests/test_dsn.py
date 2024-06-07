import os

import pexpect
from textwrap import dedent
import pytest


def test_using_dsn():
    config_content = dedent(
        """
        [alias_dsn]
        local = redis://localhost:6379/15
        """
    )
    with open("/tmp/dicerollrc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn("diceroll --dicerollrc /tmp/dicerollrc --dsn local", timeout=1)
    cli.logfile_read = open("cli_test.log", "ab")
    cli.expect(["diceroll", "localhost:6379[15]>"])
    cli.close()

    # overwrite with -n
    cli = pexpect.spawn("diceroll --dicerollrc /tmp/dicerollrc --dsn local -n 3", timeout=1)
    cli.logfile_read = open("cli_test.log", "ab")
    cli.expect(["diceroll", "localhost:6379[3]>"])
    cli.close()

    # dsn not exists
    cli = pexpect.spawn("diceroll --dicerollrc /tmp/dicerollrc --dsn ghost-dsn", timeout=1)
    cli.expect(["Could not find the specified DSN in the config file."])
    cli.close()
    assert cli.status == 1


@pytest.mark.skipif(
    not os.path.exists("/tmp/redis/redis.sock"), reason="unix socket is not found"
)
def test_using_dsn_unix():
    config_content = dedent(
        """
        [alias_dsn]
        unix = unix:///tmp/redis/redis.sock?db=3
        """
    )
    with open("/tmp/dicerollrc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn("diceroll --dicerollrc /tmp/dicerollrc --dsn unix", timeout=2)
    cli.logfile_read = open("cli_test.log", "ab")
    cli.expect(["diceroll", "redis /tmp/redis/redis.sock[3]>"])

    cli.close()
