import reflex as rx
from wac_lab.templates.template import template
from wac_lab.state.running_task import RunTask


def newtask_running() -> rx.Component:
    return rx.container(
        rx.cond(
            RunTask.running,
            rx.container(
                rx.text("Current URL: " + RunTask.running_url),
                rx.foreach(RunTask.running_actions, rx.text),
            ),
            rx.text("No task running"),
        )
    )


def newtask_buttons():
    return rx.container(
        rx.flex(
            rx.card(
                rx.button("re-generate", variant="soft"),
                on_click=RunTask.generate_new_objective,
            ),
            rx.divider(orientation="vertical", size="4"),
            rx.card("task1", on_click=RunTask.end_new_task),
            spacing="3",
        ),
        rx.divider(margin_bottom="1em", margin_top="5em"),
        rx.box(
            rx.heading("start"),
            rx.button("start task", on_click=RunTask.toggle_running_new_task),
        ),
    )
 

@template(
    route="/newtask",
    title="newtask/autogenerate",
    meta=[{"drawer-icon": "settings-2"}],
)
def newtask() -> rx.Component:
    return rx.container(
        newtask_buttons(),
    )
