from dice.utils import command_syntax
from dice.style import STYLE
from dice.commands import commands_summary
from prompt_toolkit import print_formatted_text

for command, info in commands_summary.items():
    print_formatted_text(command_syntax(command, info), style=STYLE)
