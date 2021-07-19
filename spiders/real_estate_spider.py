import os

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

from items import CraigslistScraperItem


class RealEstateSpider(scrapy.Spider):
    name = "realestate_loader"
    start_urls = ["http://newyork.craigslist.org/d/real-estate/search/rea/"]

    try:
        os.remove("results.csv")
    except OSError:
        pass

    def __init__(self):
        self.lat = ""
        self.lon = ""

    # implicit scrapy method
    # def start_requests(self):
    #     yield scrapy.Request("http://newyork.craigslist.org/d/real-estate/search/rea/", callback=self.parse)

    def parse(self, response):
        all_ads = response.xpath("//li[@class='result-row']")
        for ads in all_ads:
            ad_link = ads.xpath(".//a[@class='result-title hdrlnk']/@href").get()
            yield response.follow(url=ad_link, callback=self.parse_detail)

            loader = ItemLoader(item=CraigslistScraperItem(), selector=ads, response=response)
            loader.add_xpath("title", ".//a[@class='result-title hdrlnk']/text()")
            loader.add_xpath("price", ".//a//span[@class='result-price']/text()")
            loader.add_xpath("date", ".//time[@class='result-date']/text()")
            loader.add_xpath("ad_link", ".//a[@class='result-title hdrlnk']/@href")
            loader.add_xpath("neighborhood", ".//span[@class='result-hood']/text()")
            loader.add_value("lat", self.lat)
            loader.add_value("lon", self.lon)
            yield loader.load_item()

        # get next page ads
        next_page = response.xpath("//a[@class='button next']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        """
        Get coordinates from ad page
        """
        self.lat = response.xpath("//meta[@name='geo.position']/@content").get().split(";")[1]
        self.lon = response.xpath("//meta[@name='geo.position']/@content").get().split(";")[0]


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "DOWNLOADER_CLIENT_TLS_METHOD": "TLSv1.2",
        "FEEDS": {
            "results.csv": {"format": "csv"},
        },
    })

    process.crawl(RealEstateSpider)
    process.start()
