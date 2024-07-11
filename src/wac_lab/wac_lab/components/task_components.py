import reflex as rx
from wac_lab import styles
from wac_lab.datatypes.task_types import TaskStepInfo
from wac_lab.state.state import TaskState


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
        style=styles.task_status_button_style,
    )


def task_status_buttons(task_id: str = "") -> rx.Component:
    def _status_button(status: str, status_str: str = None, **props) -> rx.Component:
        return rx.button(
            status_str or status,
            style=styles.task_status_button_style,
            on_click=lambda: TaskState.update_task_id(status, task_id),
            **props,
        )

    return rx.container(
        # alt values "〤" ❌ "✔️" ✅
        rx.vstack(
            _status_button("Approve", status_str="✅ Approve", color_scheme="grass"),
            _status_button("Reject", status_str="❌ Reject", color_scheme="tomato"),
            _status_button("Download", status_str="📥 Download", color_scheme="mint"),
            _status_button("Reset Status"),
            # task_delete_button(),
            spacing="3",
            margin="1em",
            position="fixed",
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
        task_status_buttons(task_id=task_state.id),
    )


def task_step_card(task_step: TaskStepInfo) -> rx.Component:
    return rx.box(
        rx.container(
            rx.hstack(
                rx.heading("url"),
                rx.spacer(),
                rx.link(task_step.short_url, href=task_step.url),
            ),
            rx.flex(
                rx.heading("id"),
                rx.spacer(),
                rx.text(task_step.short_id),
            ),
            rx.box(
                rx.center(rx.image(src=task_step.image, height="auto")),
                rx.accordion.root(
                    rx.accordion.item(
                        header=rx.heading(f"step {task_step.step_idx + 1}"),
                        content=rx.box(
                            rx.foreach(
                                task_step.actions,
                                lambda action: rx.list_item(action.clean_value),
                            )
                        ),
                    ),
                    collapsible=True,
                    type="multiple",
                    variant="outline",
                    allow_toggle=True,
                ),
            ),
        ),
        rx.divider(border_color="black"),
    )
