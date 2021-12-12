import openai
import os
import requests
from data.models import ScrapedContent
from haystack.query import SearchQuerySet
from django.db.models import Q
from chat.models import GPTApi
from .translation import detect_language, translate_text_by_google
import re


def elastic_search_results(query):
    query = re.sub(r'[?|$|.|!]', r'', query)
    document = []
    sqs = SearchQuerySet().filter(Q(paragraph=query) | Q(heading=query))
    query_list = sqs[:5]
    for query in query_list:
        document.append(query.object.paragraph)
    # print(document, 'eslastic saerch response')
    return document


class BotManagement:

    def __init__(self, conversation):
        self.conversation = conversation
        self.key = conversation.bot.api.key
        self.sub_type = conversation.bot.api.subtype
        self.default_language = 'en'
        self.translated_language = None
        self.default_query = ''
        self.translated_query = ''
        self.text_response = 'some thing went wrong'
        self.json_response = {}
        self.response_status = 200
        self.gp3_type = ''

    def set_response(self):
        query = self.default_query
        lan = detect_language(self.default_query)
        if lan != self.default_language:
            self.translated_language = lan
            self.translated_query = translate_text_by_google(self.default_language, self.default_query)
            query = self.translated_query
        # always return response in english
        documents = elastic_search_results(query)
        if len(documents) >= 1:
            # print('bot answer ')
            self.search_gpt3_answers(query, documents)
            self.gp3_type = 'Answer'
        else:
            # print('bot completion ')
            self.search_GT3_Completion(query)
            self.gp3_type = 'Completion'

    #    gtp3 completion

    def search_GT3_Completion(self, query):
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
        self.parse_GT3_Completion_response(response)

    def parse_GT3_Completion_response(self, response):
        if self.translated_language:
            text_response = response.get('choices')[0].get('text')
            self.text_response = translate_text_by_google(self.translated_language, text_response)
        else:
            self.text_response = response.get('choices')[0].get('text')
        self.json_response = response

    #      gtp3 answers

    def search_gpt3_answers(self, query, document):
        examples_context, examples = self.get_latest_context()
        # print(examples, 'examples')
        # print(examples_context, 'examples context')
        response = openai.Answer.create(
            search_model="ada",
            model="curie",
            question=query,
            documents=document,
            examples_context=examples_context,
            examples=examples,
            max_tokens=5,
            stop=["\n", "<|endoftext|>"],
        )
        self.parse_gpt3_answers(response)

    def get_latest_context(self):
        if self.conversation.conversationcontent_set.last():
            examples_context = self.conversation.conversationcontent_set.last().response
            examples = [[q.query, q.response] for q in self.conversation.conversationcontent_set.all()][-2:]
            if examples_context is None:
                return self.get_default_context()
            if len(examples[0]) < 2:
                return self.get_default_context()
            return examples_context, examples
        else:
            return self.get_default_context()

    def get_default_context(self):
        examples_context = "I am safecho Bot here to help."
        examples = [['who are you?', 'what is your name']]
        return examples_context, examples

    def parse_gpt3_answers(self, response):
        if response.get('selected_documents'):
            text_response = response.get('selected_documents')[0].get('text')
            if self.translated_language:
                self.text_response = translate_text_by_google(self.translated_language, text_response)
            else:
                self.text_response = text_response
        else:
            text_response = response.get('answers')[0]
            if self.translated_language:
                self.text_response = translate_text_by_google(self.translated_language, text_response)
            else:
                self.text_response = text_response
        self.json_response = response

    def search(self, query):
        self.default_query = query
        self.set_response()
        return self.response_status, self.text_response, self.json_response, self.gp3_type
