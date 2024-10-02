import reflex as rx

from wac_lab import log


PLUGINS_SUBCLASSED = []
PLUGINS_INITIATED = []

PluginStateClassName: str = "PluginState"


def _make_plugin_state(cls, state_class: str = "PluginState"):
    PluginStateCls = getattr(cls, state_class)
    return type(
        f"{cls.__name__}State",
        (PluginStateCls, rx.State),
        dict(PluginStateCls.__dict__),
    )


def _get_plugin_name(cls: type) -> tuple[str, str]:
    def _from_getter():
        if _name := getattr(cls, "get_name", None):
            if callable(_name):
                return _name()
        return None

    if name := _from_getter():
        return name, "from_getter"
    elif name := getattr(cls, "name", None):
        return name, "from_name"
    elif name := getattr(cls, "__name__", None):
        return name, "from_class_name"

    raise ValueError("Plugin must have a name")


class Plugin:
    plugin_name: str = ""
    _should_instantiate: bool = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.validate_plugin_name()

    @classmethod
    def validate_plugin_name(cls):
        if not hasattr(cls, "plugin_name") or not cls.plugin_name:
            raise ValueError("Plugin must have a non-empty 'plugin_name' attribute")

    @classmethod
    def setup(cls, *args, **kwargs):
        if cls._should_instantiate:
            return cls(*args, **kwargs)
        return cls


class RenderableInterface:
    def render(self, view: str = "home", *args, **kwargs):
        method = getattr(self, view, None)
        if not method:
            raise ValueError(f"View method '{view}' not found in {self.plugin_name}")
        return method(*args, **kwargs)

    def home(self) -> rx.Component:
        raise NotImplementedError("Each plugin must implement a 'home' method returning a Reflex component.")


class PluginManager:
    plugins: dict[str, Plugin] = {}

    force_plugin_state_rx: bool = False

    def __repr__(self):
        out = f"<PluginManager with {len(self.plugins)} plugins>"
        for name, plugin in self.plugins.items():
            out += f"\n\t{name}->{plugin}"
        return out

    @classmethod
    def setup_plugins(cls, app: rx.App):
        import importlib

        plugins = app.plugins

        if not plugins:
            raise ValueError("No plugins provided")

        for plugin in plugins:
            if isinstance(plugin, str):
                plugin = importlib.import_module(plugin)

            if callable(plugin):
                plugin(app)

            if callable(setup_fn := getattr(plugin, "__setup__", None)):
                setup_fn(app)

            cls.register(plugin)

    @classmethod
    def register(cls, plugin: Plugin, name: str = None):
        if not name:
            name, _ = _get_plugin_name(plugin)

        if name in PluginManager.plugins:
            # raise ValueError(f"Plugin with name {name} already exists")
            log.error(f"Plugin with name {name} already exists: {PluginManager.plugins[name]}")

        # use the instance, make this optional tho in future
        PluginManager.plugins[name] = plugin.__plugin__
        log.rule(f"[cyan]{log.escape(f'PLUGIN:{name} ✅')}", align="left")

    def get_match_vals(self):
        return [(p_name, p.render()) for p_name, p in self.plugins.items()]

    def render_plugin(self, name: str, state_from: rx.State = None):
        # render_plugin is used from the buttons
        log.info(f"got state: {state_from}")
        not_found = rx.hstack(rx.text("Plugin Not Found"), rx.spinner(size="3"))
        if match_vals := self.get_match_vals():
            return rx.box(
                rx.cond(name, rx.fragment(), rx.spinner(size="3")),
                rx.flex(
                    rx.match(
                        state_from.plugin_name,
                        *match_vals,
                        not_found,
                    ),
                ),
            )
        return not_found
