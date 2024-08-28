from typing import Any

import reflex as rx

from wac_lab import pages, styles
from wac_lab.state.state import plugin_manager


class WACApp(rx.App):
    style: dict[str, Any] = styles.base_style
    stylesheets: list[str] = styles.base_stylesheets
    plugins: list[str] = ["wac_plugins.clippy"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_setup(*args, **kwargs)

    def extra_setup(self, *args, **kwargs):
        pages.api_setup(app=self)
        # let the plugin manager handle setting up the plugins,
        # the setup of plugins means instantiating the plugin classes and state
        plugin_manager.setup_plugins(app=self)


app = WACApp()
