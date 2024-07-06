import reflex as rx
from wac_lab.templates.template import template


@template(route="/health", title="health", meta=[{"drawer-icon": "heart-pulse"}])
def health() -> rx.Component:
    return rx.box(
        rx.text("✅"),
        margin_top="auto",
        margin_x="49%",
    )

