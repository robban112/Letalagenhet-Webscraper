from bs4 import BeautifulSoup

class ProviderIndexes: 
    def __init__(self, location_index=None, address_index=None, rooms_index=None, size_index=None, floor_index=None, rent_index=None,
    available_until_index=None, number_of_signed_up_index=None, image_index=0):
        self.location_index = location_index
        self.address_index = address_index
        self.rooms_index = rooms_index
        self.size_index = size_index 
        self.floor_index = floor_index 
        self.rent_index = rent_index
        self.available_until_index = available_until_index 
        self.number_of_signed_up_index = number_of_signed_up_index
        self.image_index = image_index


# def __init__(self, provider_string, request_url, appartment_url, location_index=None, 
#     address_index=None, rooms_index=None, size_index=None, floor_index=None, rent_index=None, 
#     available_until_index=None, number_of_signed_up=None, has_duplicates=False, pathToNextButton="//a[@class='btn next']",
#     move_in_date=None, image_index=0):


class Provider:
    def __init__(self, provider_string, request_url, appartment_url, provider_indexes=None, has_duplicates=False, pathToNextButton="//a[@class='btn next']",
    move_in_date=None, number_of_signed_up=None, image_prepend_url=None):
        self.request_url = request_url
        self.provider_indexes = provider_indexes
        self.appartment_url = appartment_url
        self.has_duplicates = has_duplicates
        self.pathToNextButton = pathToNextButton
        self.provider_string = provider_string
        self.move_in_date = move_in_date
        self.image_prepend_url = image_prepend_url

    # def getAppartmentForHTML(self, appart_html, index):
    #     spans = appart_html.find_all('span')
    #     a = appart_html.find_all('a')
    #     if len(spans) > 0 and len(a) > 0:
    #         location = spans[self.location_index].text
    #         address = a[self.address_index].text
    #         rooms = spans[self.rooms_index].text
    #         floor = spans[self.floor_index].text if self.floor_index != None else 'null'
    #         size = spans[self.size_index].text.replace(u'\xa0', '')
    #         rent = spans[self.rent_index].text.replace(u'\xa0', '')
    #         available_until = spans[self.available_until_index].text if self.available_until_index != None else 'null'
    #         number_of_people_signed_up = spans[self.number_of_signed_up].text if self.number_of_signed_up != None else 'null'
    #         move_in_date = spans[self.move_in_date].text if self.move_in_date != None else 'null'
    #         appartment_url = getLink(a, self)
    #         image_url = getAppartmentImage(self, appartment_url)
    #         return Appartment(location, address, rooms, floor, size, rent, number_of_people_signed_up, 
    #             appartment_url, image_url, self.self_string,available_until,move_in_date)