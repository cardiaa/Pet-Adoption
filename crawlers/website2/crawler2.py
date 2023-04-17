import scrapy
from datetime import date

class PetSpider2(scrapy.Spider):

    name = "pet2"
    animals = ['dogs', 'cats', 'rabbits', 'birds', 'equine', 'pigs', 'barnyards']

    def start_requests(self):
        for animal in self.animals:
            url = "https://bestfriends.org/adopt/adopt-our-sanctuary/{}".format(animal)
            yield scrapy.Request(url, callback = self.parse, cb_kwargs = dict(animal = animal))

    def parse(self, response, animal):
        links = response.css('.animal-card a::attr(href)').getall()
        images = response.css(".animalImage img::attr(src)").getall()
        for i, link in enumerate(links):
            params = {'image': images[i], 'link': "https://bestfriends.org" + links[i]}
            if animal == 'dogs':
                yield response.follow(link, callback = self.parse_one_dog, meta = params)
            elif animal == 'birds':
                yield response.follow(link, callback = self.parse_one_bird, meta = params)
            elif animal == 'equine':
                yield response.follow(link, callback = self.parse_one_equine, meta = params)
            else:
                yield response.follow(link, callback = self.parse_one_pet, meta = params)

        next_page = response.css('.pager__item--next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, cb_kwargs = dict(animal = animal))

    def parse_one_equine(self, response):
        name = response.css(".animal-name::text").get().strip()
        pet_info = response.css(".field-content::text").getall()
        pet_info = list(filter(lambda x: x != "", list(map(lambda x: x.strip(), pet_info))))
        animal, location, breed, color, gender = pet_info[0:5]
        story = ""
        if len(pet_info) > 5:
            story = " ".join(pet_info[5:])
        image = response.meta.get('image')
        link = response.meta.get('link')
        
        yield {
            'animal' : animal,
            'name' : name,
            'location' : location,
            'breed': breed,
            'color' : color,
            'gender' : gender,
            'story' : story,
            'image': image,
            'link': link
        }

    # Parses: cats, rabbits, pigs, barnyards
    def parse_one_pet(self, response):
        pet_info = response.css(".field-content::text").getall()
        pet_info = list(filter(lambda x: x != "", list(map(lambda x: x.strip(), pet_info))))
        image = response.meta.get('image')
        animal, location, breed, color, gender = pet_info[0:5]
        name = response.css(".animal-name::text").get().strip()
        birthday = response.css(".field-content time::text").get()
        if birthday == None:
            birthday = ""
        story = " ".join(pet_info[5:])
        link = response.meta.get('link')

        yield {
            'animal' : animal,
            'name' : name,
            'location' : location,
            'breed': breed,
            'color' : color,
            'gender' : gender,
            'birthday' : birthday,
            'story' : story,
            'image': image,
            'link': link
        }


    def parse_one_dog(self, response):
        pet_info = response.css(".field-content::text").getall()
        pet_info = list(filter(lambda x: x != "", list(map(lambda x: x.strip(), pet_info))))

        animal, location, breed, size, color, gender = pet_info[0:6]
        name = response.css(".animal-name::text").get().strip()
        birthday = response.css(".field-content time::text").get()
        if birthday == None:
            birthday = ""

        story = ""
        if len(pet_info) > 6:
            story = " ".join(pet_info[6:])

        image = response.meta.get('image')
        link = response.meta.get('link')

        yield {
            'animal' : animal,
            'name' : name,
            'location' : location,
            'size' : size,
            'breed': breed,
            'color' : color,
            'gender' : gender,
            'birthday' : birthday,
            'story' : story,
            'image': image,
            'link': link
        }


    def parse_one_bird(self, response):
        pet_info = response.css(".field-content::text").getall()
        pet_info = list(filter(lambda x: x != "", list(map(lambda x: x.strip(), pet_info))))
        image = response.meta.get('image')
        animal = pet_info[0] + " - " + pet_info[2]
        location = pet_info[1]
        name = response.css(".animal-name::text").get().strip()
        story = " ".join(pet_info[3:])
        link = response.meta.get('link')
        
        yield {
            'animal' : animal,
            'name' : name,
            'location' : location,
            'story' : story,
            'image': image,
            'link': link
        }