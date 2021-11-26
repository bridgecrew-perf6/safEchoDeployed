import openai
import os

import requests
from data.models import ScrapedContent
from haystack.query import SearchQuerySet


def elastic_search_results(query):
    document = []
    print(query, 'query')
    sqs = SearchQuerySet().filter(content_auto=query)
    query_list = sqs[:10]
    for query in query_list:
        document.append(query.object.paragraph)
    print(document)
    return document


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


def get_bot_response_gptj(bot, query):
    headers = {
        "Authorization": 'Bearer ' + bot.api.key
    }
    url = bot.api.url + 'answer'
    document = elastic_search_results(query)
    data = {
        "documents": document,
        "query": query
    }
    response = requests.post(
        url,
        json=data,
        headers=headers
    )
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
        return response
