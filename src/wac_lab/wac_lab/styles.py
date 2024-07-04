"""The style classes and constants for the Dashboard App."""

from reflex.components.radix import themes as rx

# 'tomato','red','ruby','crimson','pink','plum','purple','violet','iris','indigo','blue','cyan','teal','jade','green','grass','brown','orange','sky','mint','lime','yellow','amber','gold','bronze','gray'

THEME = rx.theme(
    appearance="inherit",
    has_background=False,
    radius="large",
    accent_color="cyan",
    scaling="100%",
    panel_background="solid",
)

STYLESHEETS = ["https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap"]

FONT_FAMILY = "Share Tech Mono"
BACKGROUND_COLOR = "var(--accent-2)"
