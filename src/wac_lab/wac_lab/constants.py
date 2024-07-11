import os

# old root dir of the example trajectory data
DATA_DIR = os.path.expanduser(os.environ.get("DATA_DIR", f"{os.getcwd()}/data"))
TASKS_DIR = os.environ.get("TASKS_DIR", f"{DATA_DIR}/tasks")

LEN_SHORT = 8
LEN_LONG = 50

IMAGE_EXT = "png"

# sorting options for index and sidebar
SORT_OPTIONS = ["id", "status", "timestamp"]
DEFAULT_SORT_BY = SORT_OPTIONS[0]
