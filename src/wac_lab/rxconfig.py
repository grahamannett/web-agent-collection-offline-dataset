import reflex as rx


class WacLabConfig(rx.Config):
    pass


config = WacLabConfig(
    app_name="wac_lab",
    telemetry_enabled=False,
)
