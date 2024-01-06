import scrapy
import os

class OrigamiSpider(scrapy.Spider):
    name = 'origami1'
    base_url = 'https://origami-database.com/label/{}'
    
    categories = {
        'Animals': [
            'armadillo', 'bat', 'bear', 'chicken', 'crane',
            'eagle', 'penguin', 'duck', 'goose', 'bison',
            'cow', 'ox', 'camel', 'domestic-cat', 'tiger',
            'cephalopod', 'crocodile', 'crab', 'deer', 'dog',
            'dolphin', 'elephant', 'donkey', 'horse', 'zebra',
            'fish', 'fox', 'toad', 'giraffe', 'goat', 'hedgehog', 'insect',
            'kangaroo', 'lizard', 'mole', 'pig', 'primate',
            'raccoon', 'rhinoceros', 'rodent', 'salamander', 'scorpion',
            'seahorse', 'seal', 'shark', 'sheep', 'sloth',
            'snail', 'snake', 'spider', 'turtle', 'whale', 'wolf'
        ],
        'Dinosaurs': [
            'Ankylosauria', 'Ceratopsians', 'Dimetrodon', 'Ornithopod',
            'Pachycephalosaur', 'Plesiosaur', 'Pterosauria', 'Sauropod',
            'Stegosauria', 'Theropod'
        ],
        'Buildings': ['building'],
        'Clothings': ['clothing'],
        'Foods': ['food'],
        'Armaments': ['armaments'],
        'Furnitures': ['furniture'],
        'Geometric Shapes': ['geometric-shape'],
        'Humanoids': ['humanoid'],
        'Landscapes': ['landscape'],
        'Fictions': ['media'],
        'Mythical Creatures': [
            'angel', 'centaur', 'cerberus', 'chimera',
            'demon', 'dragon', 'ghost', 'gorgon', 'griffin',
            'hippogriff', 'mermaid', 'pegasus', 'satyr',
            'sea serpent', 'sphinx', 'troll', 'unicorn', 'winged lion', 'winged snake'
        ],
        'Objects': ['object'],
        'Plants': ['plant'],
        'Symbols': ['symbol'],
        'Vehicles': ['vehicle']
    }

    def start_requests(self):
        for category, subcategories in self.categories.items():
            for subcategory in subcategories:
                url = self.base_url.format(subcategory)
                yield scrapy.Request(url=url, callback=self.parse, meta={'category': category, 'subcategory': subcategory})

    def parse(self, response):
        category = response.meta['category']
        subcategory = response.meta['subcategory']
        origami_list = response.css('.model-card')

        for origami in origami_list:
            image_url = origami.css('.model-card__image img::attr(src)').get()

            yield {
                'category': category,
                'subcategory': subcategory,
                'image_url': image_url,
            }

            directory = os.path.join('data', category, subcategory)
            os.makedirs(directory, exist_ok=True)

            yield scrapy.Request(url=image_url, callback=self.save_image, meta={'directory': directory})

    def save_image(self, response):
        directory = response.meta['directory']
        image_name = response.url.split('/')[-1]
        image_path = os.path.join(directory, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.body)

        self.log(f'Saved file {image_path}')
