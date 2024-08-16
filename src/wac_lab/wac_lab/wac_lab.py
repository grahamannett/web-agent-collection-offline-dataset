"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from wac_lab import pages, styles
from wac_lab.state.state import plugin_manager


class WACApp(rx.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_pages(*args, **kwargs)

    def setup_pages(self, *args, **kwargs):
        pages.api_setup(self)

        # let the plugin manager handle setting up the plugins,
        # the setup of plugins means instantiating the plugin classes and state
        if plugins := kwargs.get("plugins", None):
            plugin_manager.setup_plugins(plugins, self)


app = WACApp(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    plugins=["wac_plugins.clippy"],
)
