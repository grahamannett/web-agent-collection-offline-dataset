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


def back_button_top_right() -> rx.Component:
    return (
        rx.button(
            "🔙",
            on_click=rx.call_script("history.back()"),
            variant="soft",
            top="0",
            left="3em",
            position="absolute",
        ),
    )


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
    include_back_button: bool = False,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            return rx.box(
                rx.cond(include_back_button, back_button_top_right()),
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
                # scaling=ThemeState.scaling,
                appearance=ThemeState.appearance,
                panel_background=ThemeState.panel_background,
            )

        return theme_wrap

    return decorator
