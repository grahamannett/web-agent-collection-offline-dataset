import reflex as rx

from wac_lab.components.home_components import home_quick_buttons
from wac_lab.templates.template import template


@template(route="/", title="home")
def index() -> rx.Component:
    return rx.box(
        home_quick_buttons(),
        margin_top="10%",
    )
