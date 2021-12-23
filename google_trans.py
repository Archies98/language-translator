"""
google translator API
"""
import string
from constants import GOOGLE_LANGUAGES_TO_CODES
from exceptions import TooManyRequests, LanguageNotSupportedException, TranslationNotFound, RequestError, NotValidPayload, NotValidLength
from bs4 import BeautifulSoup
import requests


class GoogleTranslator:
    """
    class that wraps functions, which use google translate under the hood to translate text(s)
    """
    _languages = GOOGLE_LANGUAGES_TO_CODES
    supported_languages = list(_languages.keys())

    def __init__(self, source="auto", target="en"):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """

        self.__base_url = "https://translate.google.com/m"
        self._element_tag = 'div'
        self._element_query = {"class": "t0"}
        self.payload_key = 'q'  # key of text in the url
        self._url_params = {"tl": target, "sl": source}

        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source, target)
            self._url_params["tl"] = self._target
            self._url_params["sl"] = self._source

        self._alt_element_query = {"class": "result-container"}

    @staticmethod
    def get_supported_languages(as_dict=False):
        """
        return the supported languages by the google translator
        @param as_dict: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        @return: list or dict
        """
        return GoogleTranslator.supported_languages if not as_dict else GoogleTranslator._languages

    def _map_language_to_code(self, *languages):
        """
        map language to its corresponding code (abbreviation) if the language was passed by its full name by the user
        @param languages: list of languages
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        for language in languages:
            if language in self._languages.values() or language == 'auto':
                yield language
            elif language in self._languages.keys():
                yield self._languages[language]

    def translate(self, text):
        """
        function that uses google translate to translate a text
        @param text: desired text to translate
        @return: str: translated text
        """

        if self._validate_payload(text):
            text = text.strip()

            if self.payload_key:
                self._url_params[self.payload_key] = text

            response = requests.get(self.__base_url,
                                    params=self._url_params)
            if response.status_code == 429:
                raise TooManyRequests()

            if response.status_code != 200:
                raise RequestError()

            soup = BeautifulSoup(response.text, 'html.parser')

            element = soup.find(self._element_tag, self._element_query)

            if not element:
                element = soup.find(self._element_tag, self._alt_element_query)
                if not element:
                    raise TranslationNotFound(text)
                else:
                    return element.get_text(strip=True)
            else:
                return element.get_text(strip=True)

    def is_language_supported(self, *languages):
        """
        check if the language is supported by the translator
        @param languages: list of languages
        @return: bool or raise an Exception
        """
        for lang in languages:
            if lang != 'auto' and lang not in self._languages.keys():
                if lang != 'auto' and lang not in self._languages.values():
                    raise LanguageNotSupportedException(lang)
        return True

    @staticmethod
    def _validate_payload(payload, min_chars=1, max_chars=5000):
        """
        validate the target text to translate
        @param payload: text to translate
        @return: bool
        """

        if not payload or not isinstance(payload, str) or not payload.strip() or payload.isdigit():
            raise NotValidPayload(payload)

        # check if payload contains only symbols
        if all(i in string.punctuation for i in payload):
            raise NotValidPayload(payload)

        if not GoogleTranslator.__check_length(payload, min_chars, max_chars):
            raise NotValidLength(payload, min_chars, max_chars)
        return True

    @staticmethod
    def __check_length(payload, min_chars, max_chars):
        """
        check length of the provided target text to translate
        @param payload: text to translate
        @param min_chars: minimum characters allowed
        @param max_chars: maximum characters allowed
        @return: bool
        """
        return True if min_chars <= len(payload) < max_chars else False
