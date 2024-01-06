import scrapy
import os
from urllib.parse import urljoin

class OrigamiMobileSpider(scrapy.Spider):
    name = 'origami_mobile'

    origami_guide = [
        'beginner-origami',
        'easy-origami',
        'intermediate-origami',
        'holiday-origami',
        'origami-animals',
        'traditional-origami',
        'modular-origami',
        'origami-boxes',
        'origami-clothes',
        'origami-decorations',
        'origami-stationery',
        'origami-flowers',
        'origami-food',
        'origami-furniture',
        'origami-hearts',
        'origami-stars',
        'origami-toys',
        'origami-vehicles',
        'misc-origami',
    ]

    start_urls = [f'https://origami.guide/instructions/{category}/' for category in origami_guide]

    def parse(self, response):
        origami_list = response.css('a.wpupg-item-has-image')

        if not origami_list:
            self.log(f"No origami list found for URL: {response.url}")
            self.log(response.body)
        else:
            for origami in origami_list:
                page_url = origami.css('::attr(href)').get()
                yield scrapy.Request(url=urljoin(response.url, page_url), callback=self.parse_page)

    def parse_page(self, response):
        model_name = response.css('span.wpupg-item-custom-field::text').get()
        image_relative_url = response.css('div.wpupg-item-image img::attr(data-src)').get()
        image_url = urljoin(response.url, image_relative_url)

        yield {
            'model_name': model_name,
            'image_url': image_url,
        }


        yield scrapy.Request(url=image_url, callback=self.save_image, meta={'model_name': model_name})

    def save_image(self, response):
        model_name = response.meta['model_name']
        image_name = f"{model_name}.jpg"
        directory = os.path.join('data', model_name)
        os.makedirs(directory, exist_ok=True)
        image_path = os.path.join(directory, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {image_path}')
