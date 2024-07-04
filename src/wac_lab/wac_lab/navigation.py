import reflex as rx
from reflex.components import lucide

from wac_lab.styles import FONT_FAMILY


def sidebar_link(text: str, href: str, icon: str):
    return rx.link(
        rx.flex(
            rx.icon_button(
                rx.icon(tag=icon, weight=16, height=16),
                variant="soft",
            ),
            text,
            py="2",
            px="4",
            spacing="3",
            align="baseline",
            direction="row",
            font_family=FONT_FAMILY,
        ),
        href=href,
        width="100%",
        border_radius="8px",
        _hover={
            "background": "rgba(255, 255, 255, 0.1)",
            "backdrop_filter": "blur(10px)",
        },
    )


def sidebar(
    *sidebar_links,
    **props,
) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.jpg")
    heading = props.get("heading", "NOT SET")
    return rx.vstack(
        rx.drawer.close(
            rx.hstack(
                rx.image(src=logo_src, height="28px", border_radius="8px"),
                rx.heading(
                    heading,
                    font_family=FONT_FAMILY,
                    size="4",
                ),
                width="100%",
                spacing="7",
            )
        ),
        rx.divider(margin_y="3"),
        rx.vstack(
            *sidebar_links,
            padding_y="1em",
        ),
    )


def sidebar_drawer(*sidebar_links, **props) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.jpg")
    return rx.box(
        rx.hstack(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.image(
                        src=logo_src,
                        height="64px",
                        border_radius="10px",
                        margin_left="1em",
                        margin_top="1em",
                    ),
                ),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        sidebar(*sidebar_links, **props),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="18em",
                        padding="2em",
                        background_color="#FFF",
                    )
                ),
                direction="left",
            ),
        )
    )


dashboard_sidebar = sidebar_drawer(
    sidebar_link(text="Home", href="/", icon="paperclip"),
    sidebar_link(text="Tasks", href="/tasks", icon="drama"),
    sidebar_link(text="Labeler", href="/labeler", icon="tag"),
    sidebar_link(text="Settings", href="/settings", icon="settings-2"),
    logo_src="/favicon.ico",
    heading="WAC Lab",
)


def navbar(heading: str, enable_menu: bool = False) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, font_family=FONT_FAMILY, size="7"),
        rx.spacer(),
        rx.cond(
            enable_menu,
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        "Menu",
                        lucide.icon(tag="chevron_down", weight=16, height=16),
                        font_family=FONT_FAMILY,
                        variant="soft",
                    ),
                ),
                rx.menu.content(
                    rx.menu.item("Settings"),
                    rx.menu.item("Profile"),
                    rx.menu.item("Logout"),
                    font_family=FONT_FAMILY,
                    variant="soft",
                ),
                variant="soft",
                font_family=FONT_FAMILY,
            ),
        ),
        position="absolute",
        z_index="1000",
        top="0px",
        right="20%",
        padding_top="4em",
    )
