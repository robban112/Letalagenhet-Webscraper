from bs4 import BeautifulSoup
from Appartment import Appartment

def getAvailableAppartmentsFromSigtunaHem(page_content, provider):
    app_list = []
    for index, appart in enumerate(page_content.find_all("div", {"class": "object-listing-item"})):
        image_url = appart.find("img", {"class": "img-responsive"})['src']
        location = appart.find("li", {"class": "area"}).text
        address = appart.find("li", {"class": "address"}).text
        aelems = appart.find_all("a")
        rooms = None
        appartment_url = ""
        if len(aelems) > 0:
            room_string = aelems[1].text
            rooms = [int(s) for s in room_string.split() if s.isdigit()][0]
            appartment_url = aelems[1]['href']
        floor = getFloor(appart.find("li", {"class": "floor"}).text)
        rent = getNumberFromString(appart.find("li", {"class": "rent"}).text)
        size = getNumberFromString(appart.find("li", {"class": "size"}).text)
        move_in_date = appart.find("span", {"class": "date"}).text
        app_list.append(Appartment(location, address, rooms, floor, size, rent, None, appartment_url, image_url, 
            provider.provider_string, None, move_in_date))
    return app_list

def getNumberFromString(st):
    return ''.join(map(str, [int(s) for s in st.split() if s.isdigit()]))

def getFloor(f):
    if "BV" in f:
        return 0
    else:
        return getNumberFromString(f)