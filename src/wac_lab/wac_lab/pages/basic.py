import reflex as rx
from wac_lab.components.navigation import navbar
from wac_lab.templates.template import template


@template(route="/health", title="health")
def health() -> rx.Component:
    return rx.box(
        rx.text("✅"),
        margin_top="auto",
        margin_x="49%",
    )


@template(route="/settings", title="settings")
def settings() -> rx.Component:
    return rx.vstack(
        rx.box(
            navbar(heading="settings"),
            margin_top="5em",
            margin_x="25vw",
            padding="1em",
        ),
    )
