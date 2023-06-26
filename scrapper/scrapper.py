from typing import Iterator

import feedparser
import nltk
import requests
from newspaper import Article
from requests import RequestException

nltk.download('punkt')


class Scrapper:
    SEARCH_URL = 'https://news.google.com/rss/search'

    def __init__(self, queries: list[str], countries: list[dict]):
        self.QUERIES = queries
        self.COUNTRIES = countries

    def articles(self) -> Iterator[Article]:
        articles_bunch = []
        for query in self.QUERIES:
            for country in self.COUNTRIES:
                articles_bunch.append(self.__get_articles(query, country))

        plain_articles = [article for article_bunch in articles_bunch for article in article_bunch]
        for index, article in enumerate(plain_articles):
            print(f'{index}/{len(plain_articles)}')
            try:
                article = Article(article['link'])
                article.download()
                article.parse()
                article.nlp()

                yield article
            except Exception:
                continue

    def __get_articles(self, query: str, country: dict) -> list[dict]:
        params = self.__build_parameters(query, country)
        try:
            response = requests.get(self.SEARCH_URL, params=params)
            articles = feedparser.parse(response.text)
            return articles['entries']
        except RequestException:
            return []

    @staticmethod
    def __fetch_article(link: str) -> str | None:
        try:
            response = requests.get(link)
            return response.text
        except RequestException:
            return None

    @staticmethod
    def __build_parameters(query: str, country: dict) -> dict:
        return {
            'q': query,
            'ceid': country['ceid'],
            'hl': country['hl'],
            'gl': country['gl']
        }

    @staticmethod
    def __parse_article(link: str, article_html: str) -> Article:
        article = Article(link)
        article.set_html(article_html)
        article.parse()
        article.nlp()
        return article
