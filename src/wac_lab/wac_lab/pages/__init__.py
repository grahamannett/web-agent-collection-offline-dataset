from fastapi import FastAPI
from wac_lab.pages.routes import health
from wac_lab.pages.tasks import task_id_page, tasks_page
from wac_lab.pages.settings import settings
from wac_lab.pages.newtask import newtask

from wac_lab.templates.template import BACKEND_ROUTES, WS_BACKEND_ROUTES


def api_setup(api: FastAPI):
    for routes in WS_BACKEND_ROUTES:
        api.add_api_websocket_route(**routes)

    for kwargs in BACKEND_ROUTES:
        api.add_api_route(**kwargs)
