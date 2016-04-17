from scrapydemo.items import ScrapydemoItem

from scrapydemo.utils.datetime_helper import DatetimeHelper


class ItemHelper():
    _datetime_helper = DatetimeHelper()
    def build_question(self, title, create_time, author, from_url, content, domain):
        item = ScrapydemoItem()
        item['title'] = self._encode_value(title)
        item['create_time'] = self._datetime_helper.build_datetime_str(create_time)
        item['author'] = self._encode_value(author)
        item['from_url'] = self._encode_value(from_url)
        item['post_url'] = self._encode_value(from_url)
        item['rank'] = self._encode_value('')
        item['content_type'] = self._encode_value('0')
        item['content'] = self._encode_value(content)
        item['is_best'] = self._encode_value('0')
        item['domain'] = self._encode_value(domain)
        return item

    def build_answer(self, title, create_time, author, from_url, post_url, rank, content, domain):
        item = ScrapydemoItem()
        item['title'] = self._encode_value(title)
        item['create_time'] = self._datetime_helper.build_datetime_str(create_time)
        item['author'] = self._encode_value(author)
        item['from_url'] = self._encode_value(from_url)
        item['post_url'] = self._encode_value(post_url)
        item['rank'] = self._encode_value(rank)
        item['content_type'] = self._encode_value('1')
        item['content'] = self._encode_value(content)
        item['is_best'] = self._encode_value('0')
        item['domain'] = self._encode_value(domain)
        return item

    def build_best_answer(self, title, create_time, author, from_url, post_url, rank, content, domain):
        item = ScrapydemoItem()
        item['title'] = self._encode_value(title)
        item['create_time'] = self._datetime_helper.build_datetime_str(create_time)
        item['author'] = self._encode_value(author)
        item['from_url'] = self._encode_value(from_url)
        item['post_url'] = self._encode_value(post_url)
        item['rank'] = self._encode_value(rank)
        item['content_type'] = self._encode_value('1')
        item['content'] = self._encode_value(content)
        item['is_best'] = self._encode_value('1')
        item['domain'] = self._encode_value(domain)
        return item


    def _encode_value(self, value):
        if isinstance(value, unicode):
            value = value.strip().encode('utf-8')
        return value.strip()