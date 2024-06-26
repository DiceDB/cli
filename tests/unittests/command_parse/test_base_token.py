def test_ip_match(judge_command):
    def ip_valid(ip, valid):
        if valid:
            judge_command(
                f"cluster meet {ip} 6379",
                {"command": "cluster meet", "ip": ip, "port": "6379"},
            )
        else:
            judge_command(f"cluster meet {ip} 6379", None)

    ip_valid("192.168.0.1", True)
    ip_valid("255.255.255.255", True)
    ip_valid("192.168.0.256", False)
    ip_valid("192.256.0.26", False)
    ip_valid("192.255.256.26", False)
    ip_valid("0.0.0.0", True)
    ip_valid("99.999.100.1", False)
    ip_valid("300.168.0.1", False)


def test_port_match(judge_command):
    def port_valid(port, valid):
        if valid:
            judge_command(
                f"cluster meet 192.168.0.1 {port}",
                {"command": "cluster meet", "ip": "192.168.0.1", "port": port},
            )
        else:
            judge_command(f"cluster meet 192.168.0.1 {port}", None)

    port_valid("65535", True)
    port_valid("0", False)
    port_valid("1", True)
    port_valid("192.168.0.256", False)
    port_valid("65536", False)
    port_valid("65545", False)
    port_valid("65635", False)
    port_valid("66535", False)
    port_valid("75535", False)
    port_valid("1024", True)
    port_valid("6553", True)
    port_valid("99999", False)
    port_valid("99999999", False)


def test_command_with_key_in_quotes(judge_command):
    judge_command(
        'cluster keyslot "mykey"', {"command": "cluster keyslot", "key": '"mykey"'}
    )
    judge_command(
        'cluster keyslot "\\"mykey"',
        {"command": "cluster keyslot", "key": '"\\"mykey"'},
    )
    judge_command(
        'cluster keyslot "mykey "', {"command": "cluster keyslot", "key": '"mykey "'}
    )


def test_timeout(token_should_match, token_should_not_match):
    from dice.redis_grammar import TIMEOUT

    token_should_match(TIMEOUT, "1.1")
    token_should_match(TIMEOUT, "1.0")
    token_should_match(TIMEOUT, ".1")
    token_should_match(TIMEOUT, "123123.1123")
    token_should_not_match(TIMEOUT, "1.")
    token_should_not_match(TIMEOUT, ".")
    token_should_not_match(TIMEOUT, ".a")


def test_lr_const(token_should_match, token_should_not_match):
    from dice.redis_grammar import LR_CONST

    token_should_match(LR_CONST, "left")
    token_should_match(LR_CONST, "right")
    token_should_match(LR_CONST, "LEFT")
    token_should_match(LR_CONST, "RIGHT")
    token_should_not_match(LR_CONST, "righ")
    token_should_not_match(LR_CONST, "ab")
    token_should_not_match(LR_CONST, "123")
