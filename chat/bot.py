import openai
import os
import requests
from data.models import ScrapedContent
from haystack.query import SearchQuerySet
from django.db.models import Q
from chat.models import GPTApi


def elastic_search_results(query):
    document = []
    sqs = SearchQuerySet().filter(Q(paragraph=query) | Q(heading=query))
    query_list = sqs[:3]
    for query in query_list:
        document.append(query.object.paragraph)
    print(document, 'eslastic saerch response')
    return query, document


def get_gpt_j_bot_response(bot, query):
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


class BotManagement:

    def __init__(self, conversation):
        self.conversation = conversation
        self.key = conversation.bot.api.key
        self.sub_type = conversation.bot.api.subtype
        self.query = ''
        self.text_response = 'some thing went wrong'
        self.json_response = {}
        self.response_status = 200

    #   QNA

    def parse_QNA(self, response):
        self.text_response = response.get('choices')[0].get('text')
        self.json_response = response

    def search_QNA(self):
        prompt = 'Q: ' + self.query + '?\nA:'
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
        self.parse_QNA(response)

    #     answers
    def get_default_context(self):
        examples_context = "I am safecho Bot here to help."
        examples = [['who are you?', 'what is your name']]
        return examples_context, examples

    def get_latest_context(self):
        if self.conversation.conversationcontent_set.last():
            examples_context = self.conversation.conversationcontent_set.last().response
            examples = [[q.query for q in self.conversation.conversationcontent_set.all()][:2]]
            if examples_context is None:
                return self.get_default_context()
            if len(examples[0]) < 2:
                return self.get_default_context()
            return examples_context, examples
        else:
            return self.get_default_context()

    def parse_gpt3_answers(self, response):
        if response.get('selected_documents'):
            self.text_response = response.get('selected_documents')[0].get('text')
        else:
            self.text_response = response.get('answers')[0]
        self.json_response = response

    def search_gpt3_answers(self):
        qs, document = elastic_search_results(self.query)
        examples_context, examples = self.get_latest_context()
        print(examples, 'examples')
        print(examples_context, 'examples context')
        response = openai.Answer.create(
            search_model="ada",
            model="curie",
            question=self.query,
            documents=document,
            examples_context=examples_context,
            examples=examples,
            max_tokens=5,
            stop=["\n", "<|endoftext|>"],
        )
        self.parse_gpt3_answers(response)

    def search(self, query):
        self.query = query
        if self.sub_type == GPTApi.QNA:
            self.search_QNA()
        if self.sub_type == GPTApi.ANSWERS:
            self.search_gpt3_answers()
        return self.response_status, self.text_response, self.json_response
