import re
import html5lib
from html5lib import HTMLParser

from .config import Config


class Habraparser:
    _config = Config.get_instance()

    def __init__(self, body: bytes):
        self._body = body

    def process(self) -> str:
        dom: HTMLParser = html5lib.parse(self._body.decode('utf-8'))
        walker = html5lib.getTreeWalker("etree")
        stream = walker(dom)
        result = []
        script_flag = False
        for child in stream:
            if child.get('type') == 'StartTag' and child.get('name') == 'script':
                script_flag = True
            if child.get('type') == 'EndTag' and child.get('name') == 'script':
                script_flag = False
            if not script_flag:
                child = self._fix_text(child)
                child = self._fix_links(child)
            result.append(child)
        s = html5lib.serializer.HTMLSerializer(omit_optional_tags=False)
        return ''.join(s.serialize(result))

    @classmethod
    def _fix_links(cls, child):
        if child.get('type') == 'StartTag' and child.get('name') in ('a', 'use'):
            data = child.get('data', {})
            for key, value in data.items():
                _, is_mark = key
                if is_mark == 'href':
                    href = data.get(key)
                    if href:
                        new_href = cls._replace_url(href)
                        if new_href != href:
                            data[key] = new_href
        return child

    @classmethod
    def _fix_text(cls, child):
        if child.get('type') == 'Characters':
            data = child.get('data', '')
            if data:
                child['data'] = cls._add_tm_to_words(data)
        return child

    @classmethod
    def _replace_url(cls, href: str) -> str:
        return re.sub(f'^{cls._config.remote_url}', cls._config.local_url, href)

    @classmethod
    def _add_tm_to_words(cls, text: str):
        result = []
        for word in text.split(' '):
            slash_result = []
            for slash_word in word.split('/'):
                strip_word = slash_word.rstrip('.,!?:;"\'\n')
                strip_word = strip_word.lstrip('"\'')
                if len(strip_word) == 6:
                    if strip_word.isalpha():
                        slash_word = slash_word.replace(strip_word, strip_word + '™')
                slash_result.append(slash_word)
            result.append('/'.join(slash_result))
        return ' '.join(result)
