from scrapy.spiders import SitemapSpider
import re
from rustore.items import PostaCode


class PostalsSpider(SitemapSpider):
    name = "postals"
    allowed_domains = ["worldpostalcode.com"]
    sitemap_urls = ['https://worldpostalcode.com/sitemap.xml']


    def sitemap_filter(self, entries):
        for entry in entries:
            url = entry['loc']
            if any(keyword in url.lower() for keyword in [
                '/canada/',
                      '/united-states/',
                      '/argentina/',
                      '/chile/',
                      '/finland/',
                      '/hungary/',
                      '/moldova/',
                      '/portugal/',
                      '/slovenia/',
                      '/france/',
                      '/romania/',
                      '/spain/',
                      '/austria/',
                      '/czech-republic/',
                      '/germany/',
                      '/sweden/',
                      '/denmark/',
                      '/netherlands/',
                      '/italy/',
                      '/norway/',
                      '/poland/',
                      '/united-kingdom/',
                      '/japan/',
                      '/kazakhstan/',
                      '/new-zealand/',
                      '/south-africa/',
                      '/algeria/',
                      '/nigeria/',
                      '/australia/',
                      '/morocco/',
                      '/kuwait/',
                      '/thailand/',
                      '/singapore/',
                      '/armenia/'
            ]):
                yield entry



    def parse(self, response):
        codes = response.xpath('//div[@class="units noletters"]/div[@class="unit"]')
        country = response.xpath('//span[@itemprop="name"]/text()').get()
        pattern = r'var lat = "(-?\d+\.\d+)"; var lng = "(-?\d+\.\d+)"'
        match = re.search(pattern, response.text)
        if match:
            lat, lng = match.groups()
        else:
            lat = ''
            lng = ''
        for code in codes:
            item = PostaCode()
            item["country"] = country.strip()
            item["lat"] = lat.strip()
            item["lng"] = lng.strip()
            item["place"] = code.xpath('.//div[@class="place"]/text()').get().strip()
            item["postal"] = code.xpath('.//div[@class="code"]/span/text()').get().strip()
            yield item