import builtins
import glob
import ujson
import os

from .mod import Mod, mod_from_config

mods: dict[str, Mod] = {}
modified_files: dict[str, str] = {}

old_import = builtins.__import__
def new_import(name, *args, **kwargs):
    try:
        if 'mods.' in args[0]['__name__']:
            return old_import(name, *args, **kwargs)
    except IndexError:
        pass
    if (name not in modified_files) or (not mods[modified_files[name]].enabled):
        return old_import(name, *args, **kwargs)

    print(f"Importing {name} from {modified_files[name]}")
    return old_import(mods[modified_files[name]].modified_scripts[name], *args, **kwargs)

builtins.__import__ = new_import

if not os.path.exists('mods'):
    os.makedirs('mods')

def load_mods():
    for mod_path in glob.glob('mods/*'):
        if not os.path.isdir(mod_path):
            continue
        if not os.path.exists(f"{mod_path}/config.json"):
            print(f"Mod {mod_path} is missing a config.json file!")
            continue
        with open(f"{mod_path}/config.json", 'r') as fp:
            config = ujson.load(fp)
            required_params = ['name', 'version', 'author']
            missing_params = [param for param in required_params if param not in config]
            if missing_params:
                print(f"Mod {mod_path} is missing the following parameter(s) in config.json: {missing_params}")
                continue
        
        mod_class = mod_from_config(config)

        mod_key = mod_path.replace('/', '.').replace('\\', '.') # e.g. mods.howl_test_mod
        for file in glob.glob(f"{mod_path}/scripts/**/*.py", recursive=True):
            file = mod_class.add_modified_script(mod_key, file)
            file_key = file.replace(f'{mod_key}.', '') # e.g. scripts.screens.StartScreen

        if modified_files.get(file_key) is not None:
            if mods[modified_files[file_key]].priority > mod_class.priority:
                print(f"Mod {mod_path} is trying to modify the same file as {modified_files[file_key]}! Skipping loading mod...")
                continue
            print(f"Mod {mod_path} is overriding {modified_files[file_key]}")
        modified_files[file_key] = config['name']
        mods[config['name']] = mod_class

load_mods()
print('Loaded mods:', ''.join([f"\n  - {mod.name} v{mod.version} by {mod.author}" for mod in mods.values()]))