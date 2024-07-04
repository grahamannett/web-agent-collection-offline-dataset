from typing import Callable

import reflex as rx

from wac_lab.navigation import dashboard_sidebar
from wac_lab.styles import BACKGROUND_COLOR, FONT_FAMILY


def back_button_top_right() -> rx.Component:
    return (
        rx.button(
            "🔙",
            on_click=rx.call_script("history.back()"),
            top="0",
            right="0",
            variant="soft",
            position="absolute",
            margin_right="1em",
            margin_top="1em",
            height="64px",
        ),
    )


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.box(
        back_button_top_right(),
        dashboard_sidebar,
        page(),
        background_color=BACKGROUND_COLOR,
        font_family=FONT_FAMILY,
        padding_bottom="auto",
        width="auto",
        height="100%",  # or 100vh
    )
