import reflex as rx
import sqlmodel


class TaskTable(rx.Model, table=True):
    objective: str
    task_id: str

    statuses: list["StatusTable"] = sqlmodel.Relationship(back_populates="tasktable")


class StatusTable(rx.Model, table=True):
    status_id: str
    status_str: str

    task_id: str = sqlmodel.Field(foreign_key="tasktable.task_id")
