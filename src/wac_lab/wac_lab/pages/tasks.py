import reflex as rx
from wac_lab.components.component_states import task_button
from wac_lab.components.task_components import task_header_card, task_step_card
from wac_lab.state.state import TaskState, WACState
from wac_lab.templates.template import template


@template(route="/tasks", title="tasks")
def tasks_page() -> rx.Component:
    return rx.box(
        rx.heading("tasks", margin_bottom="1em"),
        rx.flex(
            rx.vstack(
                rx.foreach(
                    WACState.tasks, lambda task_id: task_button(task_folder=task_id)
                )
            ),
        ),
        spacing="1em",
        margin_x="15vw",
        margin_top="2em",
    )


@template(route="/task/[task_id]", title="task", on_load=TaskState.load_task)
def task_id_page() -> rx.Component:
    return rx.container(
        task_header_card(task_state=TaskState),
        rx.container(rx.foreach(TaskState.steps, task_step_card)),
    )
