import reflex as rx


class TaskButton(rx.ComponentState):
    task_folder: str = ""
    status: str = "PENDING"

    @classmethod
    def get_component(cls, **props):
        # Set the initial value of the State var.
        task_folder = props.pop("task_folder", None)
        if task_folder is not None:
            # Update the pydantic model to use the initial value as default.
            cls.__fields__["task_folder"].default = task_folder

        return rx.box(
            rx.button(rx.text(f"Task {task_folder}", **props), width="100%"),
            on_click=rx.redirect(f"/task/{task_folder}"),
            width="100%",
        )


class TaskComponent(rx.ComponentState):
    objective: str = ""
    url: str = ""

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        initial_objective = props.pop("task_objective", None)

        if initial_objective is not None:
            cls.__fields__["objective"].default = initial_objective

        return rx.vstack(
            rx.text("TaskComponent"),
            rx.text(cls.objective),
            rx.text("✅"),
            # **props,
        )


# not sure if the componentstate is even usable since i cant pass from rx.State
task_button = TaskButton.create
task_component = TaskComponent.create
