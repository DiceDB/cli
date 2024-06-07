import os
import re
import tempfile
from textwrap import dedent

import pexpect
import pytest
import redis

from dice.client import Client
from dice.commands import split_command_args
from dice.redis_grammar import get_command_grammar
from dice.exceptions import InvalidArguments
from dice.config import Config, config as global_config


TIMEOUT = 2
HISTORY_FILE = ".dice_history"


@pytest.fixture
def token_should_match():
    def match_func(token, tomatch):
        assert re.fullmatch(token, tomatch) is not None

    return match_func


@pytest.fixture
def token_should_not_match():
    def match_func(token, tomatch):
        assert re.fullmatch(token, tomatch) is None

    return match_func


@pytest.fixture
def judge_command():
    def judge_command_func(input_text, expect):
        if expect == "invalid":
            with pytest.raises(InvalidArguments):
                split_command_args(input_text)
            return

        command, _ = split_command_args(input_text)
        grammar = get_command_grammar(command)

        m = grammar.match(input_text)

        # test on not match
        if not expect:
            assert m is None
            return

        variables = m.variables()
        print(f"Found variables: {variables}")
        for expect_token, expect_value in expect.items():
            all_variables = variables.getall(expect_token)
            if len(all_variables) > 1:
                assert sorted(all_variables) == sorted(expect_value)
            else:
                assert variables.get(expect_token) == expect_value

    return judge_command_func


@pytest.fixture(scope="function")
def clean_redis():
    """
    Return a empty redis db. (redis-py client)
    """
    client = redis.StrictRedis(db=15)
    client.flushdb()
    return client


@pytest.fixture
def dice_client():
    return Client("127.0.0.1", "6379", db=15)


@pytest.fixture
def config():
    newconfig = Config()
    global_config.__dict__ = newconfig.__dict__
    config.raw = False
    return global_config


@pytest.fixture(scope="function")
def cli():
    """Open dice subprocess to test"""
    f = tempfile.TemporaryFile("w")
    config_content = dedent(
        """
        [main]
        log_location =
        warning = True
        """
    )
    f.write(config_content)
    f.close()
    env = os.environ
    env["PROMPT_TOOLKIT_NO_CPR"] = "1"

    child = pexpect.spawn(f"dice -n 15 --dicerc {f.name}", timeout=TIMEOUT, env=env)
    child.logfile_read = open("cli_test.log", "ab")
    child.expect(["https://github.com/dicedb/cli/issues", "127.0.0.1"])
    yield child
    child.close()


@pytest.fixture(scope="function")
def raw_cli():
    """Open dice subprocess to test"""
    TEST_diceRC = "/tmp/.dicerc.test"
    config_content = dedent(
        """
        [main]
        log_location =
        warning = True
        """
    )

    with open(TEST_diceRC, "w+") as test_dicerc:
        test_dicerc.write(config_content)

    child = pexpect.spawn(
        f"dice --raw -n 15 --dicerc {TEST_diceRC}", timeout=TIMEOUT
    )
    child.logfile_read = open("cli_test.log", "ab")
    child.expect(["https://github.com/dicedb/cli/issues", "127.0.0.1"])
    yield child
    child.close()


@pytest.fixture(scope="function")
def cli_without_warning():
    f = tempfile.TemporaryFile("w")
    config_content = dedent(
        """
        [main]
        log_location = /tmp/dice1.log
        warning = False
        """
    )
    f.write(config_content)
    f.close()

    cli = pexpect.spawn(f"dice -n 15 --dicerc {f.name}", timeout=1)
    cli.logfile_read = open("cli_test.log", "ab")
    yield cli
    cli.close()
    os.remove("/tmp/dicerc")
