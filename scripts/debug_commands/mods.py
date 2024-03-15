from scripts.debug_commands.command import Command
from scripts.debug_commands.utils import add_output_line_to_log
from scripts.mod_loader import mods
from scripts.file_loader import _FileHandler as FileHandler

class ListTotalMods(Command):
    name = "total"
    description = "Lists the total number of mods installed"
    aliases = ["t"]

    def callback(self, args):
        add_output_line_to_log(f"Total mods: {len(mods)}")

class ToggleLoader(Command):
    name = "toggle"
    description = "Toggles the mod loader (doesn't save yet)"
    aliases = ["toggle"]

    def callback(self, args):
        FileHandler.enabled = not FileHandler.enabled
        add_output_line_to_log(f"Mod loader {'en' if FileHandler.enabled else 'dis'}abled")

class ListMods(Command):
    name = "list"
    description = "List all mods"
    aliases = ["l"]

    def callback(self, args):
        for mod in mods:
            add_output_line_to_log(f"{mod['name']} by {mod['author']} - version {mod['version']}")

class ModsCommand(Command):
    name = "mods"
    description = "Manage mods"
    aliases = ["mod"]

    subCommands = [
        ListTotalMods(),
        ToggleLoader(),
        ListMods()
    ]

    def callback(self, args):
        add_output_line_to_log("Please specify a subcommand")