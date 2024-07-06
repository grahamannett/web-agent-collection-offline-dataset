"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from wac_lab import styles
from wac_lab.components.home_components import home_quick_buttons
from wac_lab.templates.template import template
from wac_lab.pages import tasks_page, task_id_page, health, settings


@template(route="/", title="home")
def index() -> rx.Component:
    return rx.box(
        home_quick_buttons(),
        margin_top="10%",
    )


app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
