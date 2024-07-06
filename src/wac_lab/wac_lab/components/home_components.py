import reflex as rx
from wac_lab.state import WACState


def home_quick_buttons() -> rx.Component:
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
