from scripts.debug_commands.command import Command
from scripts.debug_commands.utils import add_output_line_to_log
from scripts.mod_loader import mods, enabled_mods, enable_mod, disable_mod, load_bindings, main
from scripts.file_loader import _FileHandler as FileHandler

class ListTotalMods(Command):
    name = "total"
    description = "Lists the total number of mods installed"
    aliases = ["t"]

    def callback(self, args):
        add_output_line_to_log(f"Total mods: {len(mods)}" + (f" ({len(enabled_mods)} enabled)" if len(enabled_mods) != len(mods) else ""))

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
            name = mod
            mod = mods[mod]
            disabled = " (disabled)" if not name in enabled_mods else ""
            add_output_line_to_log(f"{name} by {mod['author']} - version {mod['version']}{disabled}")

class EnableMod(Command):
    name = "enable"
    description = "Enable a mod"
    aliases = ["e"]

    def callback(self, args):
        if len(args) == 0:
            add_output_line_to_log("Please specify a mod to enable")
            return
        response = enable_mod(args[0])
        if response == "already enabled":
            add_output_line_to_log("Mod already enabled")
        elif response == False:
            add_output_line_to_log("Mod not found")
        elif response is None:
            add_output_line_to_log("Multiple mods found with that name!")
        else:
            add_output_line_to_log("Mod enabled")
            load_bindings()

class DisableMod(Command):
    name = "disable"
    description = "Disable a mod"
    aliases = ["d"]

    def callback(self, args):
        if len(args) == 0:
            add_output_line_to_log("Please specify a mod to disable")
            return
        response = disable_mod(args[0])
        if response == "already disabled":
            add_output_line_to_log("Mod already disabled")
        elif response == False:
            add_output_line_to_log("Mod not found")
        elif response is None:
            add_output_line_to_log("Multiple mods found with that name!")
        else:
            add_output_line_to_log("Mod disabled")
            load_bindings()

class ReloadMods(Command):
    name = "reload"
    description = "Reloads the mod loader"
    aliases = ["r"]

    def callback(self, args):
        main()
        add_output_line_to_log("Mods reloaded")

class ModsCommand(Command):
    name = "mods"
    description = "Manage mods"
    aliases = ["mod"]

    subCommands = [
        ListTotalMods(),
        ToggleLoader(),
        ListMods(),
        EnableMod(),
        DisableMod(),
        ReloadMods()
    ]

    def callback(self, args):
        add_output_line_to_log("Please specify a subcommand")