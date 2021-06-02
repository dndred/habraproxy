import re

from bs4 import BeautifulSoup

from .config import Config

_text_tags = (
    'title',
    'div',
    'p',
    'a',
    'h1',
    'h2',
    'h3',
    'li',
    'strong',
    'span',
    'button',
    'blockquote',
    'label',
    'code',
    'td',
    'section',
    'nav',
)


class Habraparser:
    _config = Config.get_instance()

    def __init__(self, body: bytes):
        self._body = body

    def process(self) -> str:
        dom = BeautifulSoup(self._body.decode('utf-8'), 'html.parser')
        dom = self._link_middleware(dom)
        dom = self._text_middleware(dom)
        body = dom.encode(formatter=None).decode('utf-8')
        body = self._special_characters_fix(body)
        return body

    @classmethod
    def _link_middleware(cls, dom: BeautifulSoup) -> BeautifulSoup:
        for child in dom.recursiveChildGenerator():
            if 'a' == child.name:  # fix internal links
                href: str = child.attrs.get('href', '')
                if href:
                    child.attrs['href'] = cls._replace_url(href)
            if 'use' == child.name:  # for svg
                href: str = child.attrs.get('xlink:href', '')
                if href:
                    href = cls._replace_url(href)
                    child.attrs['xlink:href'] = href
        return dom

    @classmethod
    def _text_middleware(cls, dom: BeautifulSoup) -> BeautifulSoup:
        for child in dom.recursiveChildGenerator():
            if hasattr(child, 'text') and child.string:
                if child.name in _text_tags:
                    child.string = cls._add_tm_to_words(child.string)
                title = child.attrs.get('title', '')
                if title:
                    child.attrs['title'] = cls._add_tm_to_words(title)
        return dom

    @classmethod
    def _replace_url(cls, href: str) -> str:
        return re.sub(f'^{cls._config.remote_url}', cls._config.local_url, href)

    @classmethod
    def _add_tm_to_words(cls, text: str):
        result = []
        for word in text.split(' '):
            strip_word = word.rstrip('.,!?:;\n')
            if len(strip_word) == 6:
                if strip_word.isalpha():
                    word = word.replace(strip_word, strip_word + '™')
            result.append(word)
        return ' '.join(result)

    @classmethod
    def _special_characters_fix(cls, body: str) -> str:
        return body.replace('&plus', '&plus;')
