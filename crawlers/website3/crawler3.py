import scrapy

class PetSpider3(scrapy.Spider):

    name = "pet3"
    animals = ['cats', 'dogs', 
               'other_pets?species_id%5B%5D=3',  'other_pets?species_id%5B%5D=4', 'other_pets?species_id%5B%5D=5',
               'other_pets?species_id%5B%5D=9', 'other_pets?species_id%5B%5D=11', 'other_pets?species_id%5B%5D=13',
               'other_pets?species_id%5B%5D=14', 'other_pets?species_id%5B%5D=15', 'other_pets?species_id%5B%5D=16',
               'other_pets?species_id%5B%5D=18', 'other_pets?species_id%5B%5D=20', 'other_pets?species_id%5B%5D=21',]

    def start_requests(self):
        for animal in self.animals:
            yield scrapy.Request(url = "https://www.petrescue.com.au/listings/search/{}".format(animal), callback = self.parse)

    def parse(self, response):
        links = response.css('.cards-listings-preview a::attr(href)').getall()
        links = [links[i] for i in range(len(links)) if i % 2 == 0]
        images = response.css(".cards-listings-preview img::attr(data-src)").getall()

        for i, pet in enumerate(links):
            params = {'image': images[i], 'link': links[i]}
            yield response.follow(pet, callback = self.parse_one_pet, meta = params)
            
        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_one_pet(self, response):
        name = response.css(".pet-listing__content__name::text").get().strip()
        feature = response.css(".pet-listing__content__feature::text").get().strip()
        breed = response.css(".pet-listing__content__breed::text").get().strip()
        animal = breed.split(" ")[-1]
        gender = self.find_gender(breed)
        size = self.find_size(breed)
        array = response.css(".c-text-detail-block__detail::text").getall()
        array = list(map(lambda x: x.strip(), array))
        location, age, fee = array[1:4]
        story = " ".join(response.css(".personality p::text").getall()) 
        image = response.meta.get('image')
        link = response.meta.get('link')
        
        yield { 
            'animal' : animal,
            'name' : name,
            'size' : size,
            'gender' : gender,
            'breed' : breed,
            'location' : location,
            'age' : age,
            'story' : story,
            'feature' : feature,
            'fee' : fee,
            'image': image,
            'link': link
        }
          
    def find_gender(self, breed):
        if breed.upper().find("MALE") != -1:
            return "Male"
        elif breed.upper().find("FEMALE") != -1:
            return "Female"
        return ""
        
    def find_size(self, breed):
        if breed.upper().find("SMALL") != -1:
            return "Small"
        elif breed.upper().find("MEDIUM") != -1:
            return "Medium"
        elif breed.upper().find("LARGE") != -1:
            return "Large"
        return ""
    