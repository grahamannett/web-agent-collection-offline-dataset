import reflex as rx

from wac_lab import constants, logger
from wac_lab.common import file_utils


class WACState(rx.State):
    """The app state."""

    sort_by: str = "name"
    sort_direction: str = "descending"

    @rx.var
    def tasks(self) -> list[str]:
        tasks = file_utils.get_tasks(constants.TASKS_DIR)
        tasks.sort(key=lambda task: task.stat().st_ctime, reverse=True)

        if tasks[1].name == "current":
            tasks[0], tasks[1] = tasks[1], tasks[0]

        return [task.name for task in tasks]

    @rx.var
    def task_id(self) -> str:
        return self.router.page.params.get("task_id", "no pid")

    def goto_task(self, task_id: str):
        return rx.redirect(f"/tasks/{task_id}")

    def download_tasks(self):
        logger.info("Downloading tasks...")
        # return rx.download("tasks.zip", constants.TASKS_DIR)


class TaskState(rx.State):
    pass
