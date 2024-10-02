import reflex as rx

from wac_lab import constants


class DBConfig:
    db_url: str = constants.DB_URL


class WacLabConfig(rx.Config, DBConfig):
    # set these for your app
    app_name: str = "wac_lab"
    telemetry_enabled: bool = False


config = WacLabConfig()
