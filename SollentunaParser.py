from bs4 import BeautifulSoup
from Appartment import Appartment

def getAvailableAppartmentsFromSollentuna(page_content, provider):
    appartments = []
    for index, appart in enumerate(page_content.find_all("a")):
        appartment_url = 'https://www.sollentunahem.se/' + appart["href"]
        rent = appart.find("div", {"class": "c-objects__item__price"}).text
        rent = ' '.join(rent.split())
        item_info = appart.find("div", {"class": "c-objects__item__info"}).text
        address = appart.find("h1", {"class": "c-objects__item__heading"}).text
        address = ' '.join(address.split())
        number_of_people_signed_up = None
        #appartment_url = None
        available_until = None
        image_url = 'https://www.sollentunahem.se' + appart.find("img")['src']
        print(appart.find("img"))
        floor = None
        (rooms, size, location) = getItemInfo(item_info)
        appartments.append(Appartment(location, address, rooms, floor, size, rent, number_of_people_signed_up, 
            appartment_url, image_url, provider.provider_string, available_until))
    return appartments

def getItemInfo(info):
    infos = info.split('|')
    if len(infos) > 2:
        rooms = [int(s) for s in infos[0].split() if s.isdigit()][0]
        size = [int(s) for s in infos[1].split() if s.isdigit()][0]
        location = infos[2].strip()
        return (rooms, size, location)