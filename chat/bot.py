import openai
import os

import requests
from data.models import ScrapedContent
from haystack.query import SearchQuerySet
from django.db.models import Q


def elastic_search_results(query):
    document = []
    # print(query, 'query')
    sqs = SearchQuerySet().filter(Q(paragraph=query) | Q(heading=query))
    query_list = sqs[:3]
    for query in query_list:
        document.append(query.object.paragraph)
    print(document)
    return query, document


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
        "Authorization": bot.api.key
    }
    qs, document = elastic_search_results(query)
    if len(document) == 0:
        document = ["How may i help you", "Hi do you need help"]

    data = {
        "documents": document,
        "query": qs
    }
    response = requests.post(
        bot.api.url,
        json=data,
        headers=headers
    )
    print(response.status_code)
    return response.json()


def get_bot_answers(bot, query, context):
    if not context.conversationcontent_set.last():
        context_data = "In 2017, U.S. life expectancy was 78.6 years."
        queries = [["What is human life expectancy in the United States?", "78 years."]]
    else:
        context_data = context.conversationcontent_set.last().response
        queries = [[q.query for q in context.conversationcontent_set.all()][:2]]
        if len(queries) <= 2:
            queries = [["What is human life expectancy in the United States?", "78 years."]]

    qs, document = elastic_search_results(query)

    openai.api_key = bot.api.key
    response = openai.Answer.create(
        search_model="ada",
        model="curie",
        question=qs + '?',
        documents=document,
        examples_context=context_data,
        examples=queries,
        max_tokens=5,
        stop=["\n", "<|endoftext|>"],
    )
    print(response)
    return response


def upload_document_to_openapi(bot, json1):
    """
    Example Json1

    {"text": "puppy A is happy", "metadata": "emotional state of puppy A"}
    {"text": "puppy B is sad", "metadata": "emotional state of puppy B"}

    TODO: Find a way to convert the document / elastic search query to json
    """
    openai.api_key = bot.api.key
    response = openai.File.create(file=open("myfile.jsonl"), purpose='answers')

    print(response)
    return response


class BotManagement(object):
    api_key = os.getenv("OPENAI_API_KEY")

    def make_full_search_string(self, string):
        if string:
            string = '#' + string + ' OR ' + '$' + string + ' OR ' + string
        return string

    def search_response(self, query):
        openai.api_key = self.api_key
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
        return response
