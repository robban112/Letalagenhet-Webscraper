from bs4 import BeautifulSoup
from Appartment import Appartment

def getAvailableAppartmentsFromSollentuna(page_content, provider):
    app_dict = {}
    for index, appart in enumerate(page_content.find_all("article")):
        rent = appart.find("div", {"class": "c-objects__item__price"}).text
        item_info = appart.find("div", {"class": "c-objects__item__info"}).text
        address = appart.find("h1", {"class": "c-objects__item__heading"}).text
        number_of_people_signed_up = None
        appartment_url = None
        available_until = None
        floor = None
        (rooms, size, location) = getItemInfo(item_info)
        app_dict[index] = Appartment(location, address, rooms, floor, size, rent, number_of_people_signed_up, 
            appartment_url, "", provider.provider_string, available_until)

def getItemInfo(info):
    infos = info.split('|')
    if len(infos) > 2:
        rooms = [int(s) for s in infos[0].split() if s.isdigit()][0]
        size = [int(s) for s in infos[1].split() if s.isdigit()][0]
        location = infos[2].strip()
        return (rooms, size, location)