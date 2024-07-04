"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from wac_lab import logger
from wac_lab.pages.routes import health, settings
from wac_lab.pages.tasks import tasks
from wac_lab.state import WACState

from wac_lab.template import template
from wac_lab.navigation import navbar
from wac_lab.styles import THEME, STYLESHEETS


@rx.page("/tasks/[task_id]")
def task_id_page() -> rx.Component:
    return rx.heading(WACState.task_id)


def index_buttons() -> rx.Component:
    return rx.box(
        rx.heading("quick actions"),
        rx.flex(
            rx.divider(orientation="vertical", border_color="black"),
            rx.spacer(),
            rx.flex(
                rx.button("auto-generate", disabled=True),
                rx.divider(orientation="vertical", border_color="black"),
                rx.button("latest task", on_click=rx.redirect("tasks/current")),
                rx.divider(orientation="vertical", border_color="black"),
                rx.button("download tasks", on_click=WACState.download_tasks),
                spacing="3",
            ),
        ),
        rx.box(
            rx.heading("other"),
            rx.flex(
                rx.spacer(),
                rx.button("tasks", on_click=rx.redirect("/tasks")),
                rx.divider(orientation="vertical", border_color="black"),
                rx.button("health", on_click=rx.redirect("/health")),
                rx.divider(orientation="vertical", border_color="black"),
                rx.button("settings", on_click=rx.redirect("/settings")),
                spacing="3",
            ),
            margin_top="2em",
        ),
    )


@template
def index() -> rx.Component:
    return rx.box(
        navbar(heading="index"),
        index_buttons(),
        # align="center",
        margin_top="10%",
        margin_x="25vw",
        padding="1em",
    )


app = rx.App(
    theme=THEME,
    stylesheets=STYLESHEETS,
)

app.add_page(index, route="/")
app.add_page(health, route="/health")
app.add_page(settings, route="/settings")
app.add_page(tasks, route="/tasks")
