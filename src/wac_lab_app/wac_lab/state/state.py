from datetime import datetime

import reflex as rx
from PIL import Image
from sqlmodel import SQLModel, select

from wac_lab import constants, log
from wac_lab.common.file_utils import get_tasks, load_task_json_file, truncate_string
from wac_lab.datatypes.approval_status import ApprovalStatus, DefaultStatus
from wac_lab.datatypes.task_types import StepActionInfo, TaskStepInfo
from wac_lab.models import StatusTable, TaskTable
from wac_lab.plugins.plugin_manager import PluginManager


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

    steps: list[dict | TaskStepInfo] = []

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
        return DefaultStatus.emoji

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

            return StepActionInfo(
                action_idx=d_idx,
                action_type=d["action_type"],
                action_value=action_value,
                clean_value=clean_value,
            )

        self.steps = []
        for step_idx, step_data in enumerate(steps):
            image_path = f"{constants.TASKS_DIR}/{self.id}/{step_data['id']}.{constants.IMAGE_EXT}"
            image = Image.open(image_path)
            image_size: tuple[int, int] = image.size
            image = image.crop((0, 0, image_size[0], min(image_size[1], constants.IMAGE_STEP_HEIGHT)))
            status_info = self.get_status_info(step_data["id"])

            task_step_info = TaskStepInfo(
                step_idx=step_idx,
                url=step_data["url"],
                id=step_data["id"],
                short_url=truncate_string(step_data["url"], constants.LEN_LONG),
                short_id=truncate_string(step_data["id"], constants.LEN_LONG),
                image_path=image_path,
                image=image,
                actions=[get_act(di, d) for di, d in enumerate(step_data["actions"])],
                # get status from db
                status_name=status_info.name,
                status_emoji=status_info.emoji,
                status_color=status_info.color,
            )

            self.steps.append(task_step_info)

    def get_status_info(self, status_id: str) -> ApprovalStatus:
        """
        Retrieve approval status information for a given status ID.

        Args:
            status_id (str): The ID of the status to retrieve.

        Returns:
            approval_status.ApprovalStatus: The approval status information.
        """

        with rx.session() as session:
            query = select(StatusTable).where(StatusTable.status_id == status_id)
            status_info = session.exec(query).first()

        if not status_info:
            status_info = DefaultStatus

        return status_info

    def load_task(self):
        _raw_data = load_task_json_file(filepath=self.task_filepath)
        self.objective = _raw_data["objective"]
        self._setup_id(_raw_data["id"])
        self._setup_timestamp(_raw_data["timestamp"])
        self._load_steps(_raw_data["steps"])
        self.loaded = True

    def get_all_statusus(self, task_id: str):
        with rx.session() as session:
            statuses = session.exec(TaskTable.select(TaskTable.status).where(TaskTable.task_id == task_id)).all()
            log.info(f"statuses:\n{statuses}")
        return statuses

    def update_id_status(self, status_str: str, status_id: str):
        log.info(f"update: {status_id} to {status_str} {self._update_status_hooks}")
        with rx.session() as session:
            query = select(StatusTable).where(StatusTable.status_id == status_id)
            status_info = session.exec(query).first()

            if status_info:
                status_info.status = ApprovalStatus[status_str.upper()]
                log.info(f"status updated to `{status_info.status.name}`")
            else:
                status_info = StatusTable(status_id=status_id, status=ApprovalStatus[status_str.upper()])
                session.add(status_info)

            session.commit()
        return status_info
