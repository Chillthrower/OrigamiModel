import scrapy
import os
from urllib.parse import urlparse, urljoin

class OrigamiSpider(scrapy.Spider):
    name = 'origami2'
    start_urls = ['https://www.origamiway.com/paper-airplanes.shtml']

    def parse(self, response):
        origami_list = response.css('#list')

        for origami in origami_list:
            image_url = origami.css('.imageLinks img::attr(src)').get()

            yield {
                'image_url': image_url,
            }

            # differnt http scheme (http:// or https://) remeber this
            if image_url and not urlparse(image_url).scheme:
                image_url = urljoin(response.url, image_url)

            yield scrapy.Request(url=image_url, callback=self.save_image)

    def save_image(self, response):
        image_name = response.url.split('/')[-1]
        directory = os.path.join('data', 'origami', 'Airplanes')
        os.makedirs(directory, exist_ok=True)  # Create 'data/origami' if it doesn't exist

        image_path = os.path.join(directory, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {image_path}')
