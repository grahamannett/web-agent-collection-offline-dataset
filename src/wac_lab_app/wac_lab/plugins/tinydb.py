import reflex as rx
from wac_lab.plugins.plugin_manager import Plugin
from wacommon import log


class PluginState(rx.State):
    running: bool = False


class TinyDBPlugin(Plugin):
    tiny_db_path: str = "db.json"
    plugin_name: str = "clippy_plugin"

    def write_state(self, status: str, id: str):
        log.info(f"[red]TinyDBPlugin[/red] - {status}, {id}")


# this is so it wont instantiate if its rx.state but will otherwise
TinyDBPlugin = TinyDBPlugin.setup()
