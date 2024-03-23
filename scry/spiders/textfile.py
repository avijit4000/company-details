import scrapy

class TextItem(scrapy.Item):
    file = scrapy.Field()

class TextFileSpider(scrapy.Spider):
    name = "textfile"

    def start_requests(self):
        with open(r"D:\Pyn\online learning\FINAL_DATA\SCRNER_DATA\textname.txt", "r") as fil:
            allfile = fil.readlines()
            for file in allfile:
                item = TextItem()
                item['file'] = file.strip()
                yield item

