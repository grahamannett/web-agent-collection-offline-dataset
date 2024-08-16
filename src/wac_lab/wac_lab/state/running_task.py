import reflex as rx
from wac_lab.external_tools import generate
from wacommon import log


class LLMGeneratedTask(rx.Base):
    objective: str = ""


class RunTask(rx.State):
    running: bool = False
    objective: str = ""
    running_url: str = ""
    running_actions: list[str] = []

    generated_tasks: list[LLMGeneratedTask] = []

    def generate_new_objective(self):
        new_task = generate.generate_objective()
        log.info(f"new objectives: {new_task}")
        self.generated_tasks = [LLMGeneratedTask(objective=obj) for obj in new_task]

    def toggle_running_new_task(self):
        self.running = not self.running

    def end_new_task(self):
        self.running = False
