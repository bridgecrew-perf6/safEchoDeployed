from django.conf import settings
import requests
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeepL,
                             QCRI,
                             single_detection,
                             batch_detection)

# DEEPL_KEY = settings.DEEPL_KEY
# DETECT_LANGUAGE_KEY = settings.DETECT_LANGUAGE_KEY
DEEPL_KEY = 'b12bf7a9-e6f9-0a99-e84c-8b94ae14d01d'
DETECT_LANGUAGE_KEY = 'f9d9557b82d462369498fae9feb5f6e7'

text = "mien name ist jamshaid, ich bin zweiundzwanzig jhare alt. Ich liebe milch applesaft"
text_list = ["mien name ist jamshaid", "ich bin zweiundzwanzig jhare alt. Ich liebe milch applesaft"]


def detect_language(text):
    lang = single_detection(text, api_key=DETECT_LANGUAGE_KEY)
    return lang


# def translate_text_by_google(text):
#     translated = GoogleTranslator(source='auto', target='EN').translate(text=text)
#     return translated


def translate_text_by_google(lang, text):
    translated = GoogleTranslator(source='auto', target=lang).translate(text=text)
    return translated


def translate_text_list_by_google(text_list):
    translated = GoogleTranslator(source='auto', target='EN').translate_batch(text_list)
    return translated


def translate_text_by_deepL(text):
    translated = DeepL(api_key=DEEPL_KEY,
                       source="de",
                       target="en",
                       use_free_api=True
                       ).translate(text)
    return translated


def translate_text_list_by_deepL(text_list):
    translated = DeepL(api_key=DEEPL_KEY,
                       source="de",
                       target="en",
                       use_free_api=True
                       ).translate_batch(text_list)
    return translated


def translate_text_by_deepL_api(text):
    result = ''
    url = 'https://api-free.deepl.com/v2/translate'
    data = {
        "target_lang": "EN",
        "auth_key": DEEPL_KEY,
        "text": text
    }

    response = requests.post(
        url=url,
        data=data,
    )
    if response.status_code == 200:
        result = response.json()
        result = result.get('translations')

    return result

# print(translate_text_by_google(text))
# print(translate_text_list_by_google(text_list))
# print(translate_text_by_deepL(text))
# print(translate_text_list_by_deepL(text_list))
# print(translate_text_by_deepL_api(text))
# print(translate_text_by_deepL_api(text_list))
# print(detect_language('mien name ist jamshaid, ich bin zweiundzwanzig jhare alt. Ich liebe milch applesaft'))
