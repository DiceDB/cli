"""
This test ensures that all of redis-doc's markdown can be rendered.
Why do we need this?
see:
https://github.com/antirez/redis-doc/commit/02b3d1a345093c1794fd86273e9d516fffd3b819
"""

import pytest
from importlib.resources import read_text

from dice.commands import commands_summary
from dice.data import commands as commands_data
from dice.markdown import render


doc_files = []
for command, info in commands_summary.items():
    command_docs_name = "-".join(command.split()).lower()
    if info["group"] == "dice":
        continue
    doc_files.append(f"{command_docs_name}.md")


@pytest.mark.parametrize("filename", doc_files)
def test_markdown_render(filename):
    print(filename)
    doc = read_text(commands_data, filename)
    render(doc)
