import scrapy
import os
from urllib.parse import urljoin

class OrigamiMobileSpider(scrapy.Spider):
    name = 'origami_mobile'
    start_urls = ['https://en.origami-mobile.com/123/index.html']

    def parse(self, response):
        category = 'easy'
        subcategory = '123'
        origami_list = response.css('nav ul.clearfix li')

        if not origami_list:
            self.log(f"No origami list found for category: {category}, subcategory: {subcategory}, URL: {response.url}")
            self.log(response.body)  # Log HTML content for troubleshooting
        else:
            for origami in origami_list:
                page_url = origami.css('a::attr(href)').get()
                yield scrapy.Request(url=urljoin(response.url, page_url), callback=self.parse_page, meta={'category': category, 'subcategory': subcategory})

    def parse_page(self, response):
        category = response.meta['category']
        subcategory = response.meta['subcategory']
        model_name = response.css('h1::text').get()
        image_relative_url = response.css('div#stage img::attr(src)').get()
        image_url = urljoin(response.url, image_relative_url)

        yield {
            'category': category,
            'subcategory': subcategory,
            'model_name': model_name,
            'image_url': image_url,
        }

        yield scrapy.Request(url=image_url, callback=self.save_image, meta={'category': category, 'subcategory': subcategory, 'model_name': model_name})

    def save_image(self, response):
        category = response.meta['category']
        subcategory = response.meta['subcategory']
        model_name = response.meta['model_name']
        image_name = f"{model_name}.jpg"
        directory = os.path.join('data', category, subcategory, model_name)
        os.makedirs(directory, exist_ok=True)
        image_path = os.path.join(directory, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {image_path}')
