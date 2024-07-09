import reflex as rx

from wac_lab.state.state import ExternalDataset, WACState
from wac_lab.templates.template import template


def dataset_popover(dataset_info_: tuple[str, ExternalDataset]) -> rx.Component:
    dataset_key, dataset_info = dataset_info_[0], dataset_info_[1]
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(dataset_key),
        ),
        rx.popover.content(
            rx.flex(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            f"fullname: {dataset_info.dataset_name}",
                        ),
                        rx.cond(
                            dataset_info.loaded,
                            "loaded",
                            "not loaded",
                        ),
                    ),
                    rx.popover.close(
                        rx.button("Close"),
                    ),
                    spacing="3",
                ),
            ),
        ),
    )


@template(route="/settings", title="settings", meta=[{"drawer-icon": "settings-2"}])
def settings() -> rx.Component:
    return rx.vstack(
        rx.box(
            margin_top="5em",
            margin_x="25vw",
            padding="1em",
        ),
        rx.foreach(
            WACState.external_datasets,
            dataset_popover,
        ),
    )
