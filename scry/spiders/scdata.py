import scrapy
from scrapy import FormRequest
# import csv

class ScdataSpider(scrapy.Spider):
    name = "scdata"
    allowed_domains = ["www.screener.in"]
    start_urls = ["https://www.screener.in/login/"]
    # start_urls_csv = 'allcompany1.csv'
    file_path = '/path/to/your/text/file.txt'

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
        # here we define the after_login function we used in callback

    def after_login(self, response):
        # If there's a "logout" text on the page, print "Successfully logged in!"
        if response.xpath('//*[@id="nav-user-menu"]').get():
            print('Successfully logged in!')
            with open(self.start_urls_csv, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    yield scrapy.Request(url=row['company_url'])

            # with open(self.start_urls_csv, 'r') as csvfile:
            #     reader = csv.DictReader(csvfile, fieldnames=['type_of_company', 'company_name', 'company_url'])
            #     next(reader)  # Skip the header row
            #     for row in reader:
            #         yield scrapy.Request(url=row['company_url'])


class TextFileSpider(scrapy.Spider):
    name = "textfile"

    def start_requests(self):
        # Define the path to your text file
        file_path = '/path/to/your/text/file.txt'

        # Open the text file and read its contents
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Yield requests for each line in the text file
        for line in lines:
            # Remove newline characters from the end of each line
            line = line.strip()
            yield scrapy.Request(url=line, callback=self.parse)

    def parse(self, response):
        # Parse the response as needed
        # Here you can define how to extract data from the webpage
        # For demonstration, let's just print the page title
        title = response.css('title::text').get()
        print("Title:", title)