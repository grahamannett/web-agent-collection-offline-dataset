import reflex as rx

from wac_lab.state import TaskState
from wac_lab import styles


def status_button(name: str) -> rx.Component:
    return rx.button(name, style=styles.task_status_button_style)


def task_delete_button(task_id: str = None) -> rx.Component:
    return rx.box(
        rx.alert_dialog.root(
            rx.alert_dialog.trigger(
                rx.button("Delete"),
            ),
            rx.alert_dialog.content(
                rx.alert_dialog.title("Delete access"),
                rx.alert_dialog.description(
                    "Are you sure?",
                ),
                rx.flex(
                    rx.alert_dialog.cancel(
                        rx.button("Cancel"),
                    ),
                    rx.alert_dialog.action(
                        rx.button("Delete"), on_click=rx.redirect("/tasks")
                    ),
                    spacing="3",
                ),
            ),
        ),
        style=status_button_style,
    )


def task_status_buttons(task_id: str = None) -> rx.Component:
    return rx.container(
        rx.vstack(
            status_button("Approve"),
            status_button("Reject"),
            status_button("Download"),
            status_button("Reset Status"),
            # task_delete_button(),
            spacing="3",
            position="absolute",
            top="0",
            left="0",
        ),
        variant="soft",
    )


def task_extra_info(task_state: TaskState) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.text("id"),
            rx.spacer(),
            rx.text(task_state.id),
        ),
        rx.flex(
            rx.text("time started"),
            rx.spacer(),
            rx.text(task_state.timestamp),
        ),
        rx.flex(
            rx.text("full path"),
            rx.spacer(),
            rx.text(task_state.task_filepath),
        ),
    )


def task_header_card(task_state: TaskState) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.heading(task_state.objective, size="6"),
            justify="end",
            width="100%",
        ),
        rx.accordion.root(
            rx.accordion.item(
                header=task_state.status,
                content=task_extra_info(task_state),
            ),
            collapsible=True,
            type="multiple",
            variant="outline",
            allow_toggle=True,
        ),
        rx.spacer(),
        rx.divider(border_color="black"),
        rx.spacer(),
        task_status_buttons(),
    )


def task_step_card(task_step) -> rx.Component:
    return rx.box(
        rx.container(
            rx.heading("url"),
            rx.text(task_step.url),
        ),
    )
