from scripts.debug_commands.command import Command
from scripts.debug_commands.help import HelpCommand
from scripts.debug_commands.settings import ToggleCommand, SetCommand, GetCommand
from scripts.debug_commands.eval import EvalCommand
from scripts.debug_commands.fps import FpsCommand
from scripts.debug_commands.cat import CatsCommand
from scripts.debug_commands.mods import ModsCommand
from typing import List

commandList: List[Command] = [
    ToggleCommand(),
    SetCommand(),
    GetCommand(),
    EvalCommand(),
    FpsCommand(),
    CatsCommand(),
    ModsCommand()
]

helpCommand = HelpCommand(commandList)
commandList.append(helpCommand)
