import reflex as rx

# from wac_lab.plugins.plugin_manager import PluginManager
from wac_lab.state.state import WACState, plugin_manager
from wac_lab.templates.template import template


@template(route="/plugins", title="plugin-home")
def plugin_home() -> rx.Component:
    return rx.box(
        rx.heading("plugins", margin_bottom="1em"),
    )


@template(route="/plugin/[plugin_name]", title="plugin-name")
def plugin_page() -> rx.Component:
    return plugin_manager.render_plugin(WACState.plugin_name, state_from=WACState)
