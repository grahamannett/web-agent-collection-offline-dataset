from wac_lab.external_tools.cohere_api import generate_from_cohere

default_provider = "cohere"

_generate_providers = {
    "cohere": generate_from_cohere,
}


def generate_objective(provider: str = default_provider):
    return _generate_providers[provider]()


if __name__ == "__main__":
    # if you need to easily see the output of the generated tasks
    tasks = generate_objective()
    for task in tasks:
        print(task)
