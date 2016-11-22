# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_LBC.items import Annonce
from scrapy.loader import ItemLoader


class LeboncoinSpider(CrawlSpider):
    name = 'leboncoin'
    allowed_domains = ['leboncoin.fr']

    def __init__(self, url=None, *args, **kwargs):
        url = url.split(',')
        super(LeboncoinSpider, self).__init__(*args, **kwargs)
        self.start_urls = url

    rules = (
        Rule(LinkExtractor(allow=r'.*?o=\d+.*'), follow=True),
        Rule(LinkExtractor(allow=r'https:\/\/www\.leboncoin\.fr\/\w+\/\d+\.htm'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        i = ItemLoader(item=Annonce(), response=response)
        i.add_value('url', response.url)
        i.add_css('titre', 'header h1::text')
        i.add_css('prix', '.item_price .value::text')
        i.add_css('date', 'section.properties p.line::text')
        i.add_css('description', '.properties_description p.value::text')
        i.add_css('tag', '.line h2:not(.item_price) span::text, .line h2:not(.item_price) span a::text')
        return i.load_item()
