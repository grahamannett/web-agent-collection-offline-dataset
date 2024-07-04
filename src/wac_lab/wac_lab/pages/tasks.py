import reflex as rx

from wac_lab.template import template
from wac_lab.state import WACState, TaskState


class TaskComponent(rx.ComponentState):
    pass


@template
def tasks() -> rx.Component:
    return rx.box(
        rx.heading("tasks"),
        rx.vstack(rx.foreach(WACState.tasks, lambda val: rx.text(val))),
        margin_top="10%",
        margin_x="25vw",
        padding="1em",
    )
