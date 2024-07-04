import reflex as rx


def colored_box(color: str):
    return rx.box(rx.text(color))


class TaskButton(rx.ComponentState):
    task_id: str = ""
    status: str = "PENDING"

    @classmethod
    def get_component(cls, **props):
        # Set the initial value of the State var.
        task_id = props.pop("task_id", None)
        if task_id is not None:
            # Update the pydantic model to use the initial value as default.
            cls.__fields__["task_id"].default = task_id

        return rx.box(
            rx.button(rx.text(f"Task {task_id}", **props), width="100%"),
            rx.text("Status", background="lightgrey"),
            on_click=rx.redirect(f"/tasks/{task_id}"),
        )


task_button = TaskButton.create
