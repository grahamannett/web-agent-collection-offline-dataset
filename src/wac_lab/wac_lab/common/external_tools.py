import os
import requests

# simple prompt to generate tasks for time being
prompt = """Give examples of similar web tasks.  These tasks should be objectives that are completable online by an average human and require no further instruction. Only return the tasks with a new one on each line no additional output.
---
Look up recipes for Sachertorte.
Convert 100 GBP to AUD for a vacation budget.
What is the etymology of the word 'serendipity'."""

cohere_api_key = os.getenv("COHERE_KEY")
cohere_url = "https://api.cohere.com/v1"


def generate_from_cohere(
    model_name: str = "command-r-plus",
    temperature: float = 0.6,
    prompt: str = prompt,
):
    response = requests.post(
        url=f"{cohere_url}/generate",
        headers={
            "Authorization": f"Bearer {cohere_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model_name,
            "prompt": prompt,
            "temperature": temperature,
            "return_likelihoods": "NONE",
        },
    )

    response_data = response.json()
    generations = response_data["generations"][0]["text"]
    return generations.split("\n")


if __name__ == "__main__":
    # if you need to easily see the output of the generated tasks
    tasks = generate_from_cohere()
    for task in tasks:
        print(task)
