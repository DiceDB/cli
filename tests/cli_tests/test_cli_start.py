from textwrap import dedent

from packaging.version import parse as version_parse  # noqa: F401
import pexpect
import pytest


def test_start_on_connection_error():
    cli = pexpect.spawn("dice -p 12345", timeout=1)
    cli.logfile_read = open("cli_test.log", "ab")
    cli.expect(r"Error \d+ connecting to 127.0.0.1:12345. Connection refused.")
    cli.close()


def test_start_with_client_name():
    cli = pexpect.spawn("dice --client_name custom_name", timeout=2)
    cli.expect("dice")
    cli.sendline("CLIENT GETNAME")
    cli.expect("custom_name")
    cli.close()


def test_short_help_option(config):
    c = pexpect.spawn("dice -h", timeout=2)

    c.expect("Show this message and exit.")

    c = pexpect.spawn("dice -h 127.0.0.1")
    c.expect("127.0.0.1:6379>")

    c.close()


@pytest.mark.skipif("version_parse(os.environ['REDIS_VERSION']) != version_parse('5')")
def test_server_version_in_starting_on5():
    c = pexpect.spawn("dice", timeout=2)
    c.expect("redis-server  5")
    c.close()


@pytest.mark.skipif("version_parse(os.environ['REDIS_VERSION']) != version_parse('6')")
def test_server_version_in_starting_on6():
    c = pexpect.spawn("dice", timeout=2)
    c.expect("redis-server  6")
    c.close()


def test_connection_using_url(clean_redis):
    c = pexpect.spawn("dice --url redis://localhost:6379/7", timeout=2)
    c.logfile_read = open("cli_test.log", "ab")
    c.expect(["dice", "127.0.0.1:6379[7]>"])
    c.sendline("set current-db 7")
    c.expect("OK")
    c.close()


def test_connection_using_url_from_env(clean_redis, monkeypatch):
    monkeypatch.setenv("dice_URL", "redis://localhost:6379/7")
    c = pexpect.spawn("dice", timeout=2)
    c.logfile_read = open("cli_test.log", "ab")
    c.expect(["dice", "localhost:6379[7]>"])
    c.sendline("set current-db 7")
    c.expect("OK")
    c.close()


@pytest.mark.xfail(reason="current test in github action, socket not supported.")
# https://github.community/t5/GitHub-Actions/Job-service-command/td-p/33901#
# https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idservices
def test_connect_via_socket(fake_redis_socket):
    config_content = dedent(
        """
        [main]
        log_location = /tmp/dice1.log
        no_info=True
        """
    )
    with open("/tmp/dicerc", "w+") as etc_config:
        etc_config.write(config_content)

    c = pexpect.spawn("dice --dicerc /tmp/dicerc -s /tmp/test.sock", timeout=2)
    c.logfile_read = open("cli_test.log", "ab")
    c.expect("redis /tmp/test.sock")

    c.close()


def test_dice_start_with_prompt():
    cli = pexpect.spawn("dice --prompt '{host}abc{port}def{client_name}'", timeout=2)
    cli.logfile_read = open("cli_test.log", "ab")
    cli.expect("dice")
    cli.expect("127.0.0.1abc6379defNone")
    cli.close()
