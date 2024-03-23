import scrapy
from scrapy import FormRequest
import csv

class ScrdSpider(scrapy.Spider):
    name = "scrd"
    allowed_domains = ["www.screener.in"]
    start_urls = ["https://www.screener.in/login/"]
    start_urls_csv = 'D:\Pyn\online learning\FOR_WORK\Analysis_data\allcompany.csv'

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrfmiddlewaretoken']/@value").get()
        # sending FormRequest (FormRequest extends the base Request with functionality for dealing with HTML forms)
        # FormRequest.from_response() simulates a user login
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'avijit4000@gmail.com',
                'password': 'Biswas.123'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if response.xpath('//*[@id="nav-user-menu"]').get():
            print('Successfully logged in!')
            link=response.xpath('//div[@class="desktop-links"]/a[2]/@href').get()
            absolute_url = f'https://www.screener.in/{link}'
            yield scrapy.Request(url=absolute_url, callback=self.parse_country)

                # response.follow(url=link, callback=self.parse_country)
              # scrapy.Request(url=row['company_url'], callback=self.parse)

    def parse_country(self, response):
        link1=response.xpath('//*[@id="sidebar"]/div/div/a')
        for bo in link1:
            company=bo.xpath('.//text()').get()
            link2=bo.xpath('.//@href').get()
            absolute_url1 = f'https://www.screener.in/{link2}'
            yield scrapy.Request(url=absolute_url1, callback=self.parse_company, meta={'company_name':company})
    def parse_company(self, response):
        company_nam = response.request.meta['company_name']
        box2=response.xpath('//table[@class="data-table text-nowrap striped mark-visited"]/tbody/tr')
        for new in box2:
            com_name=new.xpath('.//td[2]/a/text()').get()
            company_link=new.xpath('.//td[2]/a/@href').get()
            if company_link:
                company_link = "/".join(company_link.split("/")[:3])

                company_web=f'https://www.screener.in/{company_link}'

                yield {
                    "company_nam":company_nam,
                    "com_name": com_name,
                    "company_web": company_web
                }

        if response.xpath('//div[@class="flex-row flex-space-between margin-top-16 margin-bottom-36"]/div/a'):
            page_url = response.xpath('//div[@class="flex-row flex-space-between margin-top-16 margin-bottom-36"]/div/a')
            n = len(page_url)
            next_page_url = page_url[n - 1].xpath('@href').get()
            # if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_company)
