import reflex as rx

border_radius = "var(--radius-2)"
border = f"1px solid {rx.color('gray', 5)}"
text_color = rx.color("gray", 11)
gray_color = rx.color("gray", 11)
gray_bg_color = rx.color("gray", 3)
lightgray_bg_color = rx.color("gray", 1)
accent_text_color = rx.color("accent", 10)
accent_color = rx.color("accent", 1)
accent_mg_color = rx.color("accent", 2)
accent_bg_color = rx.color("accent", 3)

green_color = rx.color("green", 11)
green_mg_color = rx.color("green", 2)
green_bg_color = rx.color("green", 3)

red_color = rx.color("red", 11)
red_mg_color = rx.color("red", 2)
red_bg_color = rx.color("red", 3)

hover_accent_color = {"_hover": {"color": accent_text_color}}
hover_accent_bg = {"_hover": {"background_color": accent_color}}
# content_width_vw = "90vw"
# sidebar_width = "36em"
# sidebar_content_width = "16em"
# max_width = "1380px"
color_box_size = ["2.25rem", "2.25rem", "2.5rem"]

task_status_button_style = {
    "color": "gold",
    "width": "100%",
    "font_family": "Comic Sans MS",
    "font_size": "1.2em",
    "font_weight": "bold",
    "box_shadow": "rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px",
    "variant": "soft",
}


template_page_style = {
    # "border_radius": "30px",
    # "radius": "large",
    # "padding_top": "auto",  # ["1em", "1em", "2em"],
    # "padding_x": "auto",  # ["auto", "auto", "2em"],
    # "flex": "1",
}

template_content_style = {
    "padding": "1em",
    "margin_bottom": "2em",
    # "width": "80vw",
    # "min_height": "90vh",
}

drawer_button_style = {
    # "margin_left": "1em",
    # "margin_top": "1em",
    "height": "64px",
    "border_radius": border_radius,  # "10px",
    "right": "1em",
    "top": "1em",
    "position": "fixed",
}


drawer_style = {
    "width": "auto",
    "top": "auto",
    "left": "auto",
    "height": "100%",
    "padding": "2em",
    "bg": lightgray_bg_color,
}

drawer_header_image_style = {
    "height": "52px",
    "border_radius": "8px",
}

link_style = {
    "color": accent_text_color,
    "text_decoration": "none",
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "white",
    "border_radius": border_radius,
}

markdown_style = {
    "code": lambda text: rx.code(text, color_scheme="gray"),
    "codeblock": lambda text, **props: rx.code_block(text, **props, margin_y="1em"),
    "a": lambda text, **props: rx.link(
        text,
        **props,
        font_weight="bold",
        text_decoration="underline",
        text_decoration_color=accent_text_color,
    ),
}

notification_badge_style = {
    "width": "1.25rem",
    "height": "1.25rem",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "position": "absolute",
    "right": "-0.35rem",
    "top": "-0.35rem",
}

ghost_input_style = {
    "--text-field-selection-color": "",
    "--text-field-focus-color": "transparent",
    "--text-field-border-width": "1px",
    "background-clip": "content-box",
    "background-color": "transparent",
    "box-shadow": "inset 0 0 0 var(--text-field-border-width) transparent",
    "color": "",
}

box_shadow_style = "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"

color_picker_style = {
    "border_radius": "max(var(--radius-3), var(--radius-full))",
    "box_shadow": box_shadow_style,
    "cursor": "pointer",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "transition": "transform 0.15s ease-in-out",
    "_active": {
        "transform": "translateY(2px) scale(0.95)",
    },
}

# STYLESHEETS = ["https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap"]
base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    "styles.css",
]

# FONT_FAMILY = "Share Tech Mono"
base_style = {
    "font_family": "Inter",
    "background_color": accent_mg_color,
}
