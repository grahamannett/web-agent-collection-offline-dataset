import reflex as rx
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


def sidebar(use_lower: bool = True):
    logo_src = "/favicon.ico"
    heading = "WAC Lab"

    # should do this with get_decorated_pages later, the icon will be on the @template()
    links_from = [
        ["Home", "/", "paperclip"],
        ["Tasks", "/tasks", "drama"],
        ["Labeler", "/labeler", "tag"],
        ["Settings", "/settings", "settings-2"],
    ]

    if use_lower:
        heading = heading.lower()
        links_from = [[name.lower(), href, icon] for name, href, icon in links_from]

    sidebar_links = [sidebar_link(name, href, icon) for name, href, icon in links_from]

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
