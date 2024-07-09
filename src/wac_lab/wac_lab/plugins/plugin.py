import reflex as rx

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


class PluginManager:
    plugins: dict[str, "Plugin"] = {}

    force_plugin_state_rx: bool = False

    def get_match_vals(self):
        return [(_plug_name, _plugin()) for _plug_name, _plugin in self.plugins.items()]

    def render_plugin(self, name: str, state_from: rx.State = None):
        return rx.box(
            rx.cond(name, rx.fragment(), rx.spinner(size="3")),
            rx.flex(
                rx.match(
                    state_from.plugin_name,
                    *self.get_match_vals(),
                    rx.hstack(rx.text("Plugin Not Found"), rx.spinner(size="3")),
                ),
            ),
        )


PluginManager = PluginManager()


class Plugin:
    plugin_name: str

    _should_instantiate: bool

    class PluginState:
        pass

    @classmethod
    def setup(cls, *args, **kwargs):
        if cls._should_instantiate:
            return cls(*args, **kwargs)
        elif kwargs != {}:
            raise ValueError("Cannot pass kwargs to plugin that does not instantiate")

        return cls

    @property
    def state(self):
        return getattr(self, "PluginState", None)

    def __init_subclass__(cls) -> None:
        name, name_from = _get_plugin_name(cls)
        is_rx = issubclass(cls, rx.State)

        if PluginManager.force_plugin_state_rx and (
            PluginStateClassName in cls.__dict__
        ):
            state_cls = _make_plugin_state(cls)
            setattr(cls, PluginStateClassName, state_cls)

        if name in PluginManager.plugins:
            raise ValueError(f"Plugin with name {name} already exists")

        cls._should_instantiate = not is_rx

        PluginManager.plugins[name] = cls if is_rx else cls()
        return super().__init_subclass__()

    def __call__(self, view: str = "home", *args, **kwargs):
        return getattr(self, view)(*args, **kwargs)
