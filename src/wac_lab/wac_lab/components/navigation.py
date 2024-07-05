import reflex as rx
from reflex.components import lucide
from wac_lab import styles


def sidebar_link(text: str, href: str, icon: str):
    return rx.link(
        rx.flex(
            rx.icon_button(
                rx.icon(
                    tag=icon,
                    weight=16,
                    height=16,
                ),
                variant="soft",
            ),
            text,
            # no idea what py and px actually are impacting.  seems like it is based on tailwind css but adjusting these values i see no change
            py="2",
            px="4",
            spacing="3",  # spacing between button and text
            align="baseline",
            direction="row",
        ),
        href=href,
        width="100%",
        # border_radius="8px",
        _hover={
            "background": "rgba(255, 255, 255, 0.1)",
            "backdrop_filter": "blur(10px)",
        },
    )


def sidebar(*sidebar_links, use_lower: bool = False, **props) -> rx.Component:
    heading = props.get("heading", "NOT SET")
    logo_src = props.get("logo_src", "/favicon.ico")

    if use_lower:
        heading = heading.lower()

    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.image(
                    src=logo_src,
                    **styles.drawer_button_style,
                ),
            ),
            rx.drawer.overlay(z_index="5"),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.drawer.close(
                            rx.hstack(
                                rx.image(
                                    src=logo_src,
                                    **styles.drawer_header_image_style,
                                ),
                                rx.heading(
                                    heading,
                                    size="8",
                                ),
                                width="auto",
                                spacing="7",
                            )
                        ),
                        rx.divider(margin_y="3"),
                        rx.vstack(
                            *sidebar_links,
                            spacing="3",
                            padding_y="1em",
                        ),
                    ),
                    **styles.drawer_style,
                )
            ),
            direction="right",
        ),
    )


dashboard_sidebar = sidebar(
    sidebar_link(text="Home", href="/", icon="paperclip"),
    sidebar_link(text="Tasks", href="/tasks", icon="drama"),
    sidebar_link(text="Labeler", href="/labeler", icon="tag"),
    sidebar_link(text="Settings", href="/settings", icon="settings-2"),
    logo_src="/favicon.ico",
    heading="WAC Lab",
    # styles=styles.drawer_style,
)


def navbar(heading: str, enable_menu: bool = False) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, size="7"),
        rx.spacer(),
        rx.cond(
            enable_menu,
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        "Menu",
                        lucide.icon(tag="chevron_down", weight=16, height=16),
                        variant="soft",
                    ),
                ),
                rx.menu.content(
                    rx.menu.item("Settings"),
                    rx.menu.item("Profile"),
                    rx.menu.item("Logout"),
                    variant="soft",
                ),
                variant="soft",
            ),
        ),
        position="absolute",
        z_index="1000",
        top="0px",
        right="20%",
        padding_top="4em",
    )
