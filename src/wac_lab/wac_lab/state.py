from datetime import datetime

import reflex as rx

from wac_lab import constants, logger
from wac_lab.common.file_utils import get_tasks, load_task_json_file, truncate_string
from wac_lab.datatypes import approval_status


class ExternalDataset(rx.State):
    loaded: bool = False
    name: str = ""


class WACState(rx.State):
    """The app state."""

    sort_by: str = "name"
    sort_direction: str = "descending"
    external_tasks: list[ExternalDataset] = []

    @rx.cached_var
    def tasks(self) -> list[str]:
        tasks = get_tasks(constants.TASKS_DIR)
        tasks.sort(key=lambda task: task.stat().st_ctime, reverse=True)

        if tasks[1].name == "current":
            tasks[0], tasks[1] = tasks[1], tasks[0]
        return [task.name for task in tasks]

    def goto_task(self, task_id: str):
        return rx.redirect(f"/tasks/{task_id}")

    def download_tasks(self):
        logger.info("Downloading tasks...")
        return rx.download("tasks.zip", constants.TASKS_DIR)


class StepActionInfo(rx.Base):
    action_idx: int
    action_type: str
    action_value: str

    clean_value: str = None


class TaskStepInfo(rx.Base):
    step_idx: int = 0
    id: str = ""
    url: str = ""
    image_path_web: str = ""
    image_path_rel: str = ""
    status: approval_status._ApprovalStatus = approval_status.

    actions: list[dict | StepActionInfo] = ""

    short_url: str = ""
    short_id: str = ""


class TaskState(rx.State):
    loaded: bool = False

    # task_instance: WACSchema = None
    objective: str = ""
    id: str = ""
    short_id: str = ""

    timestamp: str = ""
    timestamp_short: str = ""

    steps: list[dict | TaskStepInfo] = []
    # steps: list[dict] = []

    @rx.var
    def task_id_name(self) -> str:
        no_tid = "no task id"
        return self.router.page.params.get("task_id", no_tid)

    @rx.cached_var
    def task_dir(self):
        return f"{constants.TASKS_DIR}/{self.task_id_name}"

    @rx.cached_var
    def task_filepath(self) -> str:
        return f"{constants.TASKS_DIR}/{self.task_id_name}/task.json"

    @rx.var
    def status(self) -> str:
        return approval_status.DefaultStatus.emoji

    def _setup_id(self, task_id: str):
        self.id = task_id
        self.short_id = task_id[: constants.LEN_SHORT]

    def _setup_timestamp(self, timestamp: str):
        self.timestamp = timestamp
        self.timestamp_short = datetime.fromisoformat(timestamp).strftime("%m-%d %H:%M")

    def load_task(self):
        # self.filepath = self.get_filepath()
        _raw_data = load_task_json_file(filepath=self.task_filepath)
        self.objective = _raw_data["objective"]
        self._setup_id(_raw_data["id"])
        self._setup_timestamp(_raw_data["timestamp"])
        self._load_steps(_raw_data["steps"])
        self.loaded = True

    def _load_steps(self, steps: list[dict]):
        self.steps = []
        for step_idx, step_data in enumerate(steps):
            image_path_web = f"{constants.IMAGE_ASSETS}/{self.id}/{step_data['id']}.{constants.IMAGE_EXT}"
            image_path_rel = f"{constants.ROOT_DIR}/data/tasks/{self.id}/{step_data['id']}.{constants.IMAGE_EXT}"
            self.steps.append(
                TaskStepInfo(
                    step_idx=step_idx,
                    url=step_data["url"],
                    id=step_data["id"],
                    short_url=truncate_string(step_data["url"], constants.LEN_LONG),
                    short_id=truncate_string(step_data["id"], constants.LEN_LONG),
                    image_path_web=image_path_web,
                    image_path_rel=image_path_rel,
                )
            )
