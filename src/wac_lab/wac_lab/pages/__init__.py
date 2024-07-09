from fastapi import FastAPI
from wac_lab.pages.index import index
from wac_lab.pages.routes import health
from wac_lab.pages.tasks import task_id_page, tasks_page
from wac_lab.pages.settings import settings
from wac_lab.pages.newtask import newtask

from wac_lab.templates.template import api_setup
