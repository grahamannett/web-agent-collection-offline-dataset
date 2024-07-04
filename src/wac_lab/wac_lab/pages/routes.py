import reflex as rx

from wac_lab.navigation import navbar
from wac_lab.template import template


@template
def health() -> rx.Component:
    return rx.box(
        rx.text("✅"),
        margin_top="auto",
        margin_x="49%",
    )


@template
def settings() -> rx.Component:
    return rx.vstack(
        rx.box(
            navbar(heading="settings"),
            margin_top="5em",
            margin_x="25vw",
            padding="1em",
        ),
    )
