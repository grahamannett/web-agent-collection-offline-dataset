import reflex as rx
from wac_lab.state.state import WACState


def plugin_button(plugin_name: str) -> rx.Component:
    return rx.button(plugin_name, on_click=rx.redirect(f"/plugin/{plugin_name}"))


def home_quick_buttons() -> rx.Component:
    return rx.container(
        rx.box(
            rx.section(
                rx.heading("quick actions"),
                rx.flex(
                    rx.button("auto-generate", on_click=rx.redirect("newtask")),
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
        rx.box(
            rx.section(
                rx.button(rx.heading("plugins"), on_click=rx.redirect("/plugins")),
                rx.flex(
                    rx.button("clippy", on_click=rx.redirect("/clippy")),
                    rx.button(
                        "mind2web", on_click=rx.redirect("/openai"), disabled=True
                    ),
                    rx.button("cohere", on_click=rx.redirect("/cohere"), disabled=True),
                    spacing="3",
                    justify="end",
                ),
                margin_top="2em",
            )
        ),
        rx.box(
            rx.section(
                rx.heading("plugins:[alt]", on_click=rx.redirect("/plugins")),
                rx.flex(
                    rx.foreach(WACState.plugins_available, plugin_button),
                    spacing="3",
                    justify="end",
                ),
            )
        ),
        width="80%",
    )
