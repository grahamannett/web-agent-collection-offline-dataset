"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from wac_lab import pages, styles

import importlib


class WACApp(rx.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_pages()

        if plugins := kwargs.get("plugins", None):
            self.setup_plugins(plugins)

    def setup_plugins(self, plugins: list[str, callable]):
        for plugin in plugins:
            if isinstance(plugin, str):
                plugin = importlib.import_module(plugin)

            if callable(plugin):
                plugin(self)

    def setup_pages(self):
        pages.api_setup(self)


app = WACApp(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    plugins=["wac_lab.plugins.clippy"],
)
