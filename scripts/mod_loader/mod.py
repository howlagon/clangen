class Mod:
    def __init__(self,
                 name: str,
                 version: str,
                 author: str,
                 description: str = None,
                 dependencies: list = None,
                 source_url: str = None,
                 last_updated: int = None,
                 priority: int = 0
                ) -> None:
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.dependencies = dependencies
        self.source_url = source_url
        self.last_updated = last_updated
        self.enabled = True
        self.priority = priority

        self.modified_scripts = {}
    
    def add_modified_script(self, mod_key: str, file: str) -> str:
        file = file.replace('.py', '') \
                   .replace('/', '.') \
                   .replace('\\', '.')
        self.modified_scripts[file.replace(f'{mod_key}.', '')] = file
        return file
    
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
        last_updated=config.get('lastUpdated')
    )