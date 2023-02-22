from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from my_scraper.sreality_spider import SrealitySpider

settings = get_project_settings()
settings.update({
    'ITEM_PIPELINES': {
        'my_scraper.pipelines.PostgresSQLPipeline': 300,
        },
    'DOWNLOADER_MIDDLEWARES': {
        'my_scraper.middlewares.ChromeDownload': 500,
        },
    'LOG_LEVEL': 'WARNING'
})

scraped_imgs_num = 500
process = CrawlerProcess(settings)
process.crawl(SrealitySpider, max_count=scraped_imgs_num)
process.start()
print(f'Finished scraping {scraped_imgs_num} img URLs.')

