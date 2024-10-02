import reflex as rx

# from wac_lab.external_tools.generate import generate_objective
# from wac_lab.templates.template import plugin_route
from wac_lab.plugins.plugin_manager import Plugin, RenderableInterface


"""
clippy is the plugin that is used to laugh playwright

"""
from .adapters.ws_conn import ConnectionManager


class PluginState(rx.State):
    running: bool = False
    url: str = ""
    last_action: str = ""
    task: str = ""
    generated_tasks: list[str] = []

    _connection_manager = ConnectionManager()

    @rx.var
    def num_clients(self) -> int:
        return len(self._connection_manager.active_connections)

    def llm_gen_tasks(self):
        self.generated_tasks = ["task1", "task2", "task3"]
        # self.generated_tasks = generate_from_cohere()


class ClippyPlugin(Plugin, RenderableInterface):
    plugin_name: str = "clippy_plugin"
    base_text_val = "nada"

    PluginState = PluginState

    def home(self) -> rx.Component:
        return rx.box(
            rx.heading("Clippy Plugin"),
            rx.cond(
                PluginState.running,
                self.running_component(),
                self.not_running_component(),
            ),
            margin_top="10%",
        )

    def running_component(self) -> rx.Component:
        return rx.box(
            rx.heading("Clippy Plugin is running"),
            rx.text("Last action: "),
            rx.text(PluginState.last_action),
            rx.text("Current URL: "),
            rx.text(PluginState.url),
        )

    def not_running_component(self) -> rx.Component:
        return rx.box(
            rx.heading("Setup Clippy Plugin"),
            rx.input(placeholder="Enter task", on_change=PluginState.set_task),
            rx.button("Generate-LLM", on_click=PluginState.llm_gen_tasks),
            rx.foreach(PluginState.generated_tasks, rx.button),
        )


# this is so it wont instantiate if its rx.state but will otherwise
clippy_plugin = ClippyPlugin.setup()
