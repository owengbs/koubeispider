from scrapydemo.items import ScrapydemoItem


class ItemHelper():

    def build_question(self, title, create_time, author, from_url, content, domain):
        item = ScrapydemoItem()
        item['title'] = title
        item['create_time'] = create_time
        item['author'] = author
        item['from_url'] = from_url
        item['post_url'] = from_url
        item['rank'] = ''
        item['content_type'] = '0'
        item['content'] = content
        item['is_best'] = '0'
        item['domain'] = domain
        return item

    def build_answer(self, title, create_time, author, from_url, post_url, rank, content,domain):
        item = ScrapydemoItem()
        item['title'] = title
        item['create_time'] = create_time
        item['author'] = author
        item['from_url'] = from_url
        item['post_url'] = post_url
        item['rank'] = rank
        item['content_type'] = '1'
        item['content'] = content
        item['is_best'] = '0'
        item['domain'] = domain
        return item

    def build_best_answer(self, title, create_time, author, from_url, post_url, rank, content, domain):
        item = ScrapydemoItem()
        item['title'] = title
        item['create_time'] = create_time
        item['author'] = author
        item['from_url'] = from_url
        item['post_url'] = post_url
        item['rank'] = rank
        item['content_type'] = '1'
        item['content'] = content
        item['is_best'] = '1'
        item['domain'] = domain
        return item