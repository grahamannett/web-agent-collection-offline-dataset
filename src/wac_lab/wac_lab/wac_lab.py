"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from wac_lab import pages, styles
from wac_lab.components.home_components import home_quick_buttons
from wac_lab.templates.template import template


class WACApp(rx.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_pages()

    def setup_pages(self):
        pages.api_setup(self)


@template(route="/", title="home")
def index() -> rx.Component:
    return rx.box(
        home_quick_buttons(),
        margin_top="10%",
    )


app = WACApp(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
