from datetime import datetime

import reflex as rx
from PIL import Image
from wac_lab import constants
from wac_lab.common.file_utils import get_tasks, load_task_json_file, truncate_string
from wac_lab.datatypes import approval_status, task_types
from wac_lab.plugins.plugin_manager import PluginManager
from wacommon import log

plugin_manager = PluginManager()


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

    _plugin_manager: PluginManager = plugin_manager

    def load_plugin(self):
        log.info("loading plugin")

    @rx.var
    def plugins_available(self) -> rx.Component:
        return list(self._plugin_manager.plugins.keys())

    @rx.var
    def plugin_name(self) -> str:
        plugin_name = self.router.page.params.get("plugin_name", "no plugin name")
        log.info(f"setting plugin name to {plugin_name}")
        self.wacbase.set_plugin_value(plugin_name)
        return plugin_name

    @rx.var(cache=True)
    def tasks(self) -> list[str]:
        tasks = get_tasks(constants.TASKS_DIR)
        tasks.sort(key=lambda task: task.stat().st_ctime, reverse=True)

        if tasks[1].name == "current":
            tasks[0], tasks[1] = tasks[1], tasks[0]
        return [task.name for task in tasks]

    @rx.var
    def top_page(self) -> rx.Component:
        return rx.box(rx.heading("Welcome to WAC Lab!"))

    def download_tasks(self):
        log.info("Downloading tasks...")
        return rx.download("tasks.zip", constants.TASKS_DIR)

    def goto_plugin_home(self):
        return rx.box(rx.heading("plugin-home"))


class TaskState(rx.State):
    loaded: bool = False

    objective: str = ""
    id: str = ""
    short_id: str = ""

    timestamp: str = ""
    timestamp_short: str = ""

    steps: list[dict | task_types.TaskStepInfo] = []

    _update_status_hooks: list[callable] = []

    @rx.var
    def task_id_name(self) -> str:
        return self.router.page.params.get("task_id", "no task id")

    @rx.var(cache=True)
    def task_dir(self) -> str:
        return f"{constants.TASKS_DIR}/{self.task_id_name}"

    @rx.var(cache=True)
    def task_filepath(self) -> str:
        return f"{constants.TASKS_DIR}/{self.task_id_name}/task.json"

    @rx.var
    def status(self) -> str:
        return approval_status.DefaultStatus.emoji

    def _setup_id(self, task_id: str) -> None:
        self.id = task_id
        self.short_id = task_id[: constants.LEN_SHORT]

    def _setup_timestamp(self, timestamp: str) -> None:
        self.timestamp = timestamp
        self.timestamp_short = datetime.fromisoformat(timestamp).strftime("%m-%d %H:%M")

    def _load_steps(self, steps: list[dict]) -> None:
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

            return task_types.StepActionInfo(
                action_idx=d_idx,
                action_type=d["action_type"],
                action_value=action_value,
                clean_value=clean_value,
            )

        self.steps = []
        for step_idx, step_data in enumerate(steps):
            image_path = f"{constants.TASKS_DIR}/{self.id}/{step_data['id']}.{constants.IMAGE_EXT}"
            image = Image.open(image_path)
            image_size = image.size
            image = image.crop((0, 0, image_size[0], min(image_size[1], 1080)))
            self.steps.append(
                task_types.TaskStepInfo(
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
        _raw_data = load_task_json_file(filepath=self.task_filepath)
        self.objective = _raw_data["objective"]
        self._setup_id(_raw_data["id"])
        self._setup_timestamp(_raw_data["timestamp"])
        self._load_steps(_raw_data["steps"])
        self.loaded = True

    def update_id_status(self, status: str, task_id: str):
        log.info(f"update: {task_id} to {status}  {self._update_status_hooks}")
