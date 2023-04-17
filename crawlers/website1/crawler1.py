import scrapy

class PetSpider1(scrapy.Spider):

    name = "pet1"
    pets = ['cat', 'dog']

    def start_requests(self):
        for animal in self.pets:
            url = "https://petsmartcharities.org/adopt-a-pet/find-a-pet?species={}".format(animal)
            yield scrapy.Request(url, callback = self.parse, cb_kwargs = dict(animal = animal))

    def parse(self, response, animal):
        links = response.css('.find-a-pet-link a::attr(href)').getall()
        images = response.css('.aap-pet-photo a img::attr(src)').getall()
        for i, link in enumerate(links):
            params = {'animal': animal, 'image': images[i], 'link': links[i]}
            yield response.follow(link, callback = self.parse_one_pet, meta = params)
            
        next_page = response.css('.aap-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse, cb_kwargs = dict(animal = animal))

    def parse_one_pet(self, pet):
        #extract want you want
        animal = pet.meta.get('animal')
        image = pet.meta.get('image')
        name = pet.css('h1::text').get()
        breed = pet.css('h4::text').get()
        location = pet.css('.shelter::text').get() + ' City: ' + pet.css('.city::text').get()
        age = pet.css('.pet-detail-page__info__pet__age p::text').getall()[1]
        gender = pet.css('.pet-detail-page__info__pet__gender p::text').getall()[1]
        color = pet.css('.pet-detail-page__info__pet__color p::text').getall()[1]
        try:
            size = pet.css('.pet-detail-page__info__pet__size p::text').getall()[1]
        except IndexError:
            size = ""
        story = ' '.join(pet.css('.pet-detail-page__info__story p::text').getall())
        adoption_center = pet.css('h3::text').getall()[1]
        link = pet.meta.get('link')

        yield {
            'animal' : animal,
            'name' : name,
            'size' : size,
            'gender' : gender, 
            'breed' : breed,
            'location' : location,
            'age' : age,
            'story' : story,
            'color' : color,
            'adoption_center' : adoption_center,
            'image': image, 
            'link': link
        }
        
        
        
        
