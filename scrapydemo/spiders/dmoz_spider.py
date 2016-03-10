# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider

from scrapydemo.items import ScrapydemoItem
class DmozSpider(BaseSpider):
	name="demo"
	allowed_domains=["www.babytree.com"]
	start_urls=[
     "http://www.babytree.com/ask/myqa__view~mlist,tab~D"
	]

	def parse(self, response):
		for href in response.xpath("//ul/li[@class='list-item']/p[@class='list-title']/a/@href"):
			url = href.extract()
			yield scrapy.Request(url,callback=self.parse_item,meta={'from_url':url})

		# for href in response.xpath("//div[@class='pagejump']/a/@href"):
		# 	url = response.urljoin(href.extract())
		# 	yield scrapy.Request(url, callback=self.parse)

	def parse_item(self, response):
		from_url = response.meta['from_url']
		items = list()
		sels = response.selector.xpath("//div[@class='qa-article section-module']")
		if len(sels) >1:
			raise " sels  length is more than one"
		title_selector = sels[0]
		item = ScrapydemoItem()
		title = title_selector.xpath("./div[@class='qa-title']/h1/text()")[0].extract()
		item['title'] = title
		item['create_time'] = title_selector.xpath("./div[@class='qa-related']/div[@class='qa-contributor']/span[@class='source']/abbr/text()")[0].extract()
		item['author'] = title_selector.xpath("./div[@class='qa-related']/div[@class='qa-contributor']/ul/li/a/span/text()").extract()
		item['from_url'] = from_url
		item['post_url'] = from_url
		item['rank'] = "0"
		item['content_type'] = "0"
		item['content'] = title
		items.append(item)


		for answer in response.selector.xpath("//ul[@class='qa-answer-list']/li[@class='answer-item']"):
			answer_item = ScrapydemoItem()
			answer_item['title'] = title
			answer_item['author'] = answer.xpath("./ul[@class='qa-meta']/li[@class='username']/a/span/text()")[0].extract()
			answer_item['create_time'] = answer.xpath("./ul[@class='qa-meta']/li[@class='timestamp']/span/text()")[0].extract()
			answer_item['from_url'] = from_url
			answer_item['post_url'] = from_url
			answer_item['rank'] = " "
			answer_item['content_type'] = "1"
			answer_item['content'] = answer.xpath("./div[@class='answer-text']/text()")[0].extract()
			items.append(answer_item)


		for  more_answer_url in response.selector.xpath("//span[@id='more_answer_page']/div[@class='pagejump']/a/@href"):
			answer_item =  scrapy.Request(more_answer_url,callback=self.parse_answers,meta={'from_url':from_url})
			items.append(answer_item)

		return items





	#def parse_answers(url):



#	def parse_more_answer(self, response):

