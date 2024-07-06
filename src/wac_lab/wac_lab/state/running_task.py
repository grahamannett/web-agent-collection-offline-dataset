import reflex as rx

from wac_lab import logger
from wac_lab.common.api_utils import generate_from_cohere


class LLMGeneratedTask(rx.Base):
    objective: str = ""


class RunTask(rx.State):
    running: bool = False
    objective: str = ""
    running_url: str = ""
    running_actions: list[str] = []

    generated_tasks: list[LLMGeneratedTask] = []

    def generate_new_objective(self):
        logger.info("regenerating...")

    def toggle_running_new_task(self):
        self.running = not self.running

    def end_new_task(self):
        self.running = False
