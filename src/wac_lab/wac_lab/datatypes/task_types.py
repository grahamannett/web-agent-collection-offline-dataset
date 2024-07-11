from PIL import Image
import reflex as rx
from wac_lab.datatypes import approval_status


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


class TaskInfo(rx.Base):
    objective: str = ""
    id: str = ""
    short_id: str = ""

    timestamp: str = ""
    timestamp_short: str = ""

    steps: list[dict | TaskStepInfo] = []
