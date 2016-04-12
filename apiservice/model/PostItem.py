class PostItem(object):
    #code
    def __init__(self, docid, content, createtime, from_url, post_url, author, rank):
        self.docid = docid
        self.content = content
        self.createtime = createtime
        self.from_url = from_url
        self.post_url = post_url
        self.author = author
        self.rank = rank
