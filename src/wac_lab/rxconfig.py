import os
import reflex as rx


class DBConfig:
    db_url: str = os.environ.get("DB_URL")  # "sqlite:///reflex.db"


class WacLabConfig(rx.Config, DBConfig):
    # set these for your app
    app_name: str = "wac_lab"
    telemetry_enabled: bool = False


config = WacLabConfig()
