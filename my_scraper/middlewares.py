from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import time

class ChromeDownload:
    options = Options()
    options.add_argument('--no-sandbox')
    options.headless = True
    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    
    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        return HtmlResponse(request.url, encoding='utf-8', body=self.driver.page_source.encode('utf-8'))
