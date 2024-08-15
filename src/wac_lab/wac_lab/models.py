import reflex as rx
import sqlmodel


class Task(rx.Model, table=True):
    objective: str
    task_id: str

    statuses: list["Status"] = sqlmodel.Relationship(back_populates="task")



class Status(rx.Model, table=True):
    status_id: str
    state: str

    task_id: str = sqlmodel.Field(foreign_key="task.task_id")

