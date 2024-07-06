import reflex as rx
from wac_lab.templates.template import template


@template(route="/health", title="health", meta=[{"drawer-icon": "heart-pulse"}])
def health() -> rx.Component:
    return rx.box(
        rx.text("✅"),
        margin_top="auto",
        margin_x="49%",
    )


@template(route="/settings", title="settings", meta=[{"drawer-icon": "settings-2"}])
def settings() -> rx.Component:
    return rx.vstack(
        rx.box(
            margin_top="5em",
            margin_x="25vw",
            padding="1em",
        ),
    )
