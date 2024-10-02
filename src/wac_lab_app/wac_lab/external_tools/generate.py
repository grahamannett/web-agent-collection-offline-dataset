from wac_lab.constants import DEFAULT_EXTERNAL_LLM
from wac_lab.external_tools.cohere_api import generate_from_cohere


def generate_objective(provider: str = DEFAULT_EXTERNAL_LLM):
    breakpoint()
    _generate_providers = {
        "cohere": generate_from_cohere,
    }
    return None

    # resp = _generate_providers[provider]()
    # breakpoint()
    # return resp


if __name__ == "__main__":
    # if you need to easily see the output of the generated tasks
    tasks = generate_objective()
    for task in tasks:
        print(task)
