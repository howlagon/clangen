import builtins
import glob
import ujson
import os

mods = {}
modified_files = {}

old_import = builtins.__import__
def new_import(name, *args, **kwargs):
    try:
        if 'mods.' in args[0]['__name__']:
            return old_import(name, *args, **kwargs)
    except IndexError:
        pass
    if name in modified_files:
        print(f"Importing {name} from {modified_files[name]}")
        return old_import(modified_files[name], *args, **kwargs)
    return old_import(name, *args, **kwargs)

builtins.__import__ = new_import

if not os.path.exists('mods'):
    os.makedirs('mods')

def load_mods():
    for mod in glob.glob('mods/*'):
        if not os.path.isdir(mod):
            continue
        if not os.path.exists(f"{mod}/config.json"):
            print(f"Mod {mod} is missing a config.json file")
            continue
        with open(f"{mod}/config.json", 'r') as f:
            config = ujson.load(f)
            required_params = ['name', 'version', 'author']
            missing_params = [param for param in required_params if param not in config]
            if missing_params:
                print(f"Mod {mod} is missing the following parameter(s) in config.json: {missing_params}")
                continue
        
        key = mod.replace('/', '.').replace('\\', '.')
        for file in glob.glob(f"{mod}/scripts/**/*.py", recursive=True):
            file = file.replace('.py', '') \
                            .replace('/', '.') \
                            .replace('\\', '.')
        modified_files[file.replace(f'{key}.', '')] = file
        mods[config['name']] = config

load_mods()
print('Loaded mods:', ''.join([f"\n  - {mod["name"]} v{mod["version"]} by {mod["author"]}" for mod in mods.values()]))