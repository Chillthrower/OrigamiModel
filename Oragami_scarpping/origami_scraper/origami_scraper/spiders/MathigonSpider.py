from urllib.parse import urljoin
import scrapy
import os

class OrigamiSpider(scrapy.Spider):
    name = 'origami'
    base_url = 'https://mathigon.org/origami/{}'
    
    categories = {
        'shapes': [
            # Platonic Solids
            'tetrahedron',
            'cube',
            'octahedron',
            'dodecahedron',
            'icosahedron',
            
            # Archimedean Solids
            'truncated-tetrahedron',
            'cuboctahedron',
            'truncated-hexahedron',
            'truncated-octahedron',
            'rhombicuboctahedron',
            'truncated-cuboctahedron',
            'snub-cube',
            'icosidodecahedron',
            'truncated-dodecahedron',
            'truncated-icosahedron',
            'rhombicosidodecahedron',
            'truncated-icosidodecahedron',
            'snub-dodecahedron',
            
            # Stars and Compounds
            'intersecting-tetrahedra',
            'intersecting-cubes',
            'intersecting-dodecahedra',
            'icosahedron-and-dodecahedron',
            'icosahedron-and-icosidodecahedron',
            'spiked-icosahedron',
            'stellated-icosahedron',
            'two-tetrahedra-and-a-sunken-cube',
            'intersection-of-four-cubes',
            'three-cubes-and-two-tetrahedra',
            
            # Beautiful Origami
            'origami-ball',
            'windmill',
            'intersecting-planes',
            'ornamental-omega',
            
            # Dragons (specific shapes not listed)
            'dragons'
        ]
    }

    def start_requests(self):
        for category, shapes in self.categories.items():
            for shape in shapes:
                url = self.base_url.format(shape)
                yield scrapy.Request(url=url, callback=self.parse, meta={'category': category, 'shape': shape})

    def parse(self, response):
        category = response.meta['category']
        shape = response.meta['shape']
        origami_list = response.css('a.origami-model')

        for origami in origami_list:
            image_url = origami.css('div.origami-image::attr(data-bg)').get()
            if image_url:
                image_url = image_url.split(',')[1].strip("url()\"'")

                # Construct the absolute URL for the image
                absolute_image_url = urljoin(response.url, image_url)

                model_name = origami.css('h3::text').get()

                yield {
                    'category': category,
                    'shape': shape,
                    'model_name': model_name,
                    'image_url': absolute_image_url,
                }

                # Create directory based on category and shape
                directory = os.path.join('data', category, shape)
                os.makedirs(directory, exist_ok=True)

                # Download the image
                yield scrapy.Request(url=absolute_image_url, callback=self.save_image, meta={'directory': directory, 'model_name': model_name})

    def save_image(self, response):
        directory = response.meta['directory']
        model_name = response.meta['model_name']
        image_name = f"{model_name}.jpg"
        image_path = os.path.join(directory, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {image_path}')
