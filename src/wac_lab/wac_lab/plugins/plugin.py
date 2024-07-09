import reflex as rx

PLUGINS_SUBCLASSED = []
PLUGINS_INITIATED = []


class PluginManager:
    plugins: list["Plugin"] = []

    def list_plugins(self):
        return [p.name for p in self.plugins]


PluginManager = PluginManager()


class Plugin:
    name: str

    def __init_subclass__(cls) -> None:
        PluginManager.plugins.append(cls())
        return super().__init_subclass__()
