class Mod:
    def __init__(self,
                 name: str,
                 version: str,
                 author: str,
                 mod_key: str = None,
                 description: str = None,
                 dependencies: list = None,
                 source_url: str = None,
                 hash_url: str = None,
                 commit_hash: str = None,
                 priority: int = 0,
                 toggleable: bool = True
                ) -> None:
        self.name = name
        self.version = version
        self.author = author
        self.mod_key = mod_key
        self.description = description
        self.dependencies = dependencies
        self.source_url = source_url
        self.hash_url = hash_url
        self.commit_hash = commit_hash
        self.enabled = True
        self.priority = priority
        self.toggleable = toggleable

        self.modified_files = {}
        self.modified_scripts = {}
    
    def add_modified_script(self, mod_key: str, file: str) -> str:
        file = file.replace('.py', '') \
                   .replace('/', '.') \
                   .replace('\\', '.')
        self.modified_scripts[file.replace(f'{mod_key}.', '')] = file
        return file
    
    def add_modified_file(self, old_path, new_path):
        self.modified_files[old_path] = new_path

    def disable(self) -> None:
        self.enabled = False
    
    def enable(self) -> None:
        self.enabled = True

def mod_from_config(config: dict) -> Mod:
    return Mod(
        name=config['name'],
        version=config['version'],
        author=config['author'],
        description=config.get('description'),
        dependencies=config.get('dependencies'),
        source_url=config.get('sourceUrl'),
        hash_url=config.get('hashUrl'),
        commit_hash=config.get('commitHash'),
        priority=config.get('priority', 0),
        toggleable=config.get('toggleable', True)
    )