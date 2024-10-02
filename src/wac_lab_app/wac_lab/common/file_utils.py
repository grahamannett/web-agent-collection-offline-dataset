import json
from functools import cache
from pathlib import Path
from typing import List


def as_path(path: str | Path) -> Path:
    """
    Converts the input path to a `Path` object if it is a string.

    Args:
        path (str | Path): The input path to be converted.

    Returns:
        Path: The converted `Path` object.

    """
    if isinstance(path, str):
        path = Path(path)

    return path


def get_tasks(tasks_dir: str) -> List[Path]:
    """
    Get a list of tasks from the specified directory.

    Args:
        tasks_dir (str): The directory path where the tasks are located.

    Returns:
        List[Path]: A list of Path objects representing the tasks.

    """
    return [f for f in as_path(tasks_dir).iterdir() if f.is_dir()]


def get_task_file_path(
    task_id: str, tasks_dir: str | Path, filename: str = "task.json"
) -> str:
    """
    Get the file path for a task.

    Args:
        task_id (str): The ID of the task.
        tasks_dir (str | Path): The directory where the tasks are stored.
        filename (str, optional): The name of the file. Defaults to "task.json".

    Returns:
        str: The file path for the task.
    """
    filepath = as_path(tasks_dir) / task_id / filename
    return str(filepath.resolve())


@cache
def load_task_json_file(
    filepath: str = None, id: str = None, get_path_func=None
) -> dict:
    """
    Load a JSON file and return its contents as a dictionary.

    Args:
        filepath (str, optional): The path to the JSON file. If not provided, it will be determined using the `id` and `get_path_func` parameters.
        id (str, optional): The identifier used to determine the file path if `filepath` is not provided.
        get_path_func (callable, optional): A function that takes the `id` as input and returns the file path.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    if (filepath is None) and (id is not None) and (get_path_func is not None):
        filepath = get_path_func(id)

    if isinstance(filepath, Path):
        filepath = str(filepath.resolve())

    with open(filepath) as f:
        data = json.load(f)

    return data


def truncate_string(input_str: str, max_length: int, suffix_str: str = "...") -> str:
    """
    Truncates a string to a specified maximum length and appends a suffix if necessary.

    Args:
        input_str (str): The input string to be truncated.
        max_length (int): The maximum length of the truncated string.
        suffix_str (str, optional): The suffix to be appended if the string is truncated. Defaults to "...".

    Returns:
        str: The truncated string.

    """
    return (
        f"{input_str[:max_length]}{suffix_str}"
        if len(input_str) > max_length
        else input_str
    )
