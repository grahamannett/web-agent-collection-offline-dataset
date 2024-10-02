import os

import requests

from wacommon import log


cohere_api_key = os.getenv("COHERE_KEY")
cohere_url = "https://api.cohere.com"

# simple prompt to generate tasks for time being
prompt_for_generate = """Give examples of similar web tasks.  These tasks should be objectives that are completable online by an average human and require no further instruction. Only return the tasks with a new one on each line no additional output.
---
Look up recipes for Sachertorte.
Convert 100 GBP to AUD for a vacation budget.
What is the etymology of the word "serendipity"."""


model_name_for_generate = "command-r-plus"


def _parse_v1_chat_resp(response: dict):
    """
    {
    "response_id": "1a3..., "text": "Res..., "generation_id": "a97c...
    "chat_history": [{
        "role": "USER", "message": "Giv...
        },{
        "role": "CHATBOT", "message": "Res...
    }],
    "finish_reason": "COMPLETE",
    "meta": {
        "api_version": {"version": "1"},
        ...
    """
    text = response["text"]
    return text


def _make_v1_generate_request(prompt: str, temperature: float, model_name: str):
    return {
        "prompt": prompt,
        "temperature": temperature,
        "model": model_name,
        "return_likelihoods": "NONE",
        "stream": False,
    }


def _parse_v1_generate_resp(response: dict):
    return response["generations"][0]["text"]


def generate_from_cohere(
    model_name: str = model_name_for_generate,
    prompt: str = prompt_for_generate,
    temperature: float = 0.6,
    endpoint: str = "v1/chat",
    **kwargs,
):
    endpoint_parser = {
        "v1/chat": _parse_v1_chat_resp,
        "v1/generate": _parse_v1_generate_resp,
    }

    parser = endpoint_parser[endpoint]

    log.info(f"making cohere request for prompt: {prompt}")
    response = requests.post(
        url=f"{cohere_url}/{endpoint}",
        headers={
            "Authorization": f"bearer {cohere_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "stream": False,
            "message": prompt,
            "temperature": temperature,
            # "model": model_name,
        },
    )

    response_data = response.json()
    generations = parser(response_data)
    return generations.split("\n")
