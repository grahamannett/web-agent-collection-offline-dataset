import reflex as rx
from wac_lab import constants


class WacLabConfig(rx.Config):
    # set these for your app
    app_name: str = "wac_lab"
    db_url: str = "sqlite:///reflex.db"  # constants.database_path
    telemetry_enabled: bool = False


config = WacLabConfig()
