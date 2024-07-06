from PIL import Image
from datetime import datetime

import reflex as rx

from wac_lab import constants, logger
from wac_lab.common.file_utils import get_tasks, load_task_json_file, truncate_string
from wac_lab.datatypes import approval_status


class ExternalDataset(rx.Base):
    loaded: bool = False
    dataset_name: str = ""
    short_name: str = ""


class WACState(rx.State):
    """The app state."""

    sort_by: str = "name"
    sort_direction: str = "descending"
    external_datasets: dict[str, ExternalDataset] = {
        "mind2web": ExternalDataset(
            dataset_name="osunlp/Multimodal-Mind2Web",
            short_name="mind2web",
        ),
    }

    @rx.cached_var
    def tasks(self) -> list[str]:
        tasks = get_tasks(constants.TASKS_DIR)
        tasks.sort(key=lambda task: task.stat().st_ctime, reverse=True)

        if tasks[1].name == "current":
            tasks[0], tasks[1] = tasks[1], tasks[0]
        return [task.name for task in tasks]

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
    image_path: str = ""
    image: Image.Image = None

    status: approval_status._ApprovalStatus = approval_status.Approved

    actions: list[StepActionInfo] = ""

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

    def _load_steps(self, steps: list[dict]):
        def get_act(d_idx, d):
            action_type = d["action_type"]
            action_value = clean_value = "unknown"
            if action_type == "click":
                action_value = f"pos({d['x']},{d['y']})"
                clean_value = f"click at {action_value}"
            elif action_type in ["type", "enter"]:
                action_value = d["value"]
                clean_value = "press enter"
            elif action_type in ["input"]:
                action_value = f'"{d["value"]}"'
                clean_value = "type " + action_value

            return StepActionInfo(
                action_idx=d_idx,
                action_type=d["action_type"],
                action_value=action_value,
                clean_value=clean_value,
            )

        self.steps = []
        for step_idx, step_data in enumerate(steps):
            image_path = f"{constants.ROOT_DIR}/data/tasks/{self.id}/{step_data['id']}.{constants.IMAGE_EXT}"
            image = Image.open(image_path)
            image_size = image.size
            image = image.crop((0, 0, image_size[0], min(image_size[1], 1080)))
            self.steps.append(
                TaskStepInfo(
                    step_idx=step_idx,
                    url=step_data["url"],
                    id=step_data["id"],
                    short_url=truncate_string(step_data["url"], constants.LEN_LONG),
                    short_id=truncate_string(step_data["id"], constants.LEN_LONG),
                    image_path=image_path,
                    image=image,
                    actions=[
                        get_act(di, d) for di, d in enumerate(step_data["actions"])
                    ],
                )
            )

    def load_task(self):
        # self.filepath = self.get_filepath()
        _raw_data = load_task_json_file(filepath=self.task_filepath)
        self.objective = _raw_data["objective"]
        self._setup_id(_raw_data["id"])
        self._setup_timestamp(_raw_data["timestamp"])
        self._load_steps(_raw_data["steps"])
        self.loaded = True

    def update_task_id(self, status: str, task_id: str):
        logger.info(f"should update: {task_id} to {status}")

