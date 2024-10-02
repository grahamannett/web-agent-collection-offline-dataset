import reflex as rx
import sqlmodel

from wac_lab.datatypes.approval_status import ApprovalStatus


class TaskTable(rx.Model, table=True):
    objective: str
    task_id: str
    # TODO: statuses: list["StatusTable"] = sqlmodel.Relationship(back_populates="tasktable")


class StatusTable(rx.Model, table=True):
    status_id: str
    status: ApprovalStatus


# model tools
def upsert_any(table: type[rx.Model], data: rx.Model, field_name: str):
    with rx.session() as session:
        # Check if the data already exists in the table
        stmt = table.select().where(getattr(table, field_name) == getattr(data, field_name))
        result = session.exec(stmt).first()

        if result:
            # Update the existing data
            for key, value in data.dict().items():
                setattr(result, key, value)
        else:
            # Insert the new data
            session.add(data)

        session.commit()

    return result
