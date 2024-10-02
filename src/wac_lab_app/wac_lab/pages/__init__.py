# Have to import all the routes so that they are used in the application
from wac_lab.pages.index import index
from wac_lab.pages.newtask_route import newtask
from wac_lab.pages.plugin_route import plugin_home, plugin_page
from wac_lab.pages.routes import health
from wac_lab.pages.settings_route import settings
from wac_lab.pages.tasks_route import task_id_page, tasks_page
from wac_lab.templates.template import api_setup
