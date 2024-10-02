from functools import wraps
from typing import Callable

import reflex as rx

# from wac_lab.styles import BACKGROUND_COLOR, FONT_FAMILY
from wac_lab import styles
from wac_lab.components.navigation import sidebar

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]

TEMPLATED_ROUTES = []
BACKEND_ROUTES = []
WS_BACKEND_ROUTES = []


class ThemeState(rx.State):
    """The state for the theme of the app.

    available accent colors:
    'tomato','red','ruby','crimson','pink','plum','purple','violet','iris','indigo','blue','cyan',
    'teal','jade','green','grass','brown','orange','sky','mint','lime','yellow','amber','gold','bronze','gray'

    """

    accent_color: str = "cyan"
    gray_color: str = "gray"
    radius: str = "none"
    scaling: str = "100%"
    appearance: str = "inherit"
    panel_background: str = "solid"
    has_background: bool = True


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | dict | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            return rx.box(
                sidebar(),
                rx.container(
                    page_content(),
                    **styles.template_content_style,
                ),
                **styles.template_page_style,
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=ThemeState.has_background,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
                radius=ThemeState.radius,
                scaling=ThemeState.scaling,
                appearance=ThemeState.appearance,
                panel_background=ThemeState.panel_background,
            )

        return theme_wrap

    return decorator


def plugin_route(route: str, is_ws: bool = False, **kwargs):
    """
    Decorator function used to attach a backend route to the application.

    Args:
        route (str): The route path for the backend route.
        is_ws (bool, optional): Indicates whether the route is a WebSocket route. Defaults to False.
        **kwargs: Additional keyword arguments to be passed to the route configuration.

    Returns:
        Callable: The decorated function.

    Example:
        @plugin_route('/api/users', is_ws=False, methods=['GET'])
        def get_users():
            # Function implementation
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        route_config = {"path": route, "endpoint": wrapper, **kwargs}
        routes_holder = WS_BACKEND_ROUTES if is_ws else BACKEND_ROUTES
        routes_holder.append(route_config)

        return wrapper

    return decorator


def api_setup(app: rx.App):
    for routes in WS_BACKEND_ROUTES:
        app.api.add_api_websocket_route(**routes)

    for routes in BACKEND_ROUTES:
        app.api.add_api_route(**routes)
