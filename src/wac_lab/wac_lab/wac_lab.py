"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from wac_lab import styles
from wac_lab.components.navigation import navbar
from wac_lab.state import WACState
from wac_lab.templates.template import template


def index_buttons() -> rx.Component:
    return rx.container(
        rx.box(
            rx.section(
                rx.heading("quick actions"),
                rx.flex(
                    rx.button("auto-generate", disabled=True),
                    rx.button("latest task", on_click=rx.redirect("tasks/current")),
                    rx.button("download tasks", on_click=WACState.download_tasks),
                    spacing="3",
                    justify="end",
                ),
            ),
        ),
        rx.box(
            rx.section(
                rx.heading("other"),
                rx.flex(
                    rx.button("tasks", on_click=rx.redirect("/tasks")),
                    rx.divider(orientation="vertical", border_color="black"),
                    rx.button("health", on_click=rx.redirect("/health")),
                    rx.divider(orientation="vertical", border_color="black"),
                    rx.button("settings", on_click=rx.redirect("/settings")),
                    spacing="3",
                    justify="end",
                ),
                margin_top="2em",
            )
        ),
        width="80%",
    )


@template(route="/", title="index")
def index() -> rx.Component:
    return rx.box(
        index_buttons(),
        navbar(heading="HEYO", enable_menu=True),
        margin_top="10%",
    )


app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
