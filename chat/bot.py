import openai
import os

import requests

GPTJ_headers = {"Authorization": os.getenv("FOREFRONT_GPTJ_API_KEY")}
GPTJ_URL = 'https://7344f216-search-qa-safecho.forefront.link/'

def get_bot_response(query):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = 'Q: ' + query + '?\nA:'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    print(response)
    return response


def get_bot_response_gptj(document, query):
    data = {
        "documents": document,
        "query": query
    }

    response = requests.post(
        GPTJ_URL + 'answer',
        json=data,
        headers=GPTJ_headers
    )
    print(response.json())
    return response.json()


class BotManagement(object):
    api_key = os.getenv("OPENAI_API_KEY")

    def make_full_search_string(self, string):
        if string:
            string = '#' + string + ' OR ' + '$' + string + ' OR ' + string
        return string

    def search_response(self, query):
        openai.api_key = self.api_key
        prompt = 'Q: ' + query + '?\nA:'
        # prompt = query
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        print(response)
        return response
