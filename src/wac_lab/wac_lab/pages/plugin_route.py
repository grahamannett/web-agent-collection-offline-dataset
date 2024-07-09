import reflex as rx

from wac_lab.plugins.plugin import PluginManager
from wac_lab.state.state import WACState
from wac_lab.templates.template import template


@template(route="/plugins", title="plugin-home")
def plugin_home() -> rx.Component:
    return rx.box(
        rx.heading("plugins", margin_bottom="1em"),
    )


@template(route="/plugin/[plugin_name]", title="plugin-name")
def plugin_page() -> rx.Component:
    return PluginManager.render_plugin(WACState.plugin_name, state_from=WACState)
