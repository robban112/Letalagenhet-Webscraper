from bs4 import BeautifulSoup
from Model.Appartment import Appartment

def getAvailableAppartmentsFromSigtunaHem(page_content, provider):
    app_list = []
    for index, appart in enumerate(page_content.find_all("div", {"class": "row"})):
        if not fieldsAvailable(appart):
            continue
        image_url = appart.find("img", {"class": "img-responsive"})['src']
        location = appart.find("li", {"class": "area"}).text
        address = appart.find("li", {"class": "address"}).text
        aelems = appart.find_all("a")
        rooms = None
        appartment_url = ""
        if len(aelems) > 1:
            room_string = aelems[1].text
            rooms_list = [int(s) for s in room_string.split() if s.isdigit()]
            if len(rooms_list) > 0:
                rooms = [int(s) for s in room_string.split() if s.isdigit()][0]
            appartment_url = aelems[1]['href']
            if not appartment_url[:4] == 'http':
                continue
        floor = getFloor(appart.find("li", {"class": "floor"}).text)
        rent = getNumberFromString(appart.find("li", {"class": "rent"}).text)
        size = getNumberFromString(appart.find("li", {"class": "size"}).text)
        move_in_date = appart.find("span", {"class": "date"}).text
        appartment = Appartment(location, address, rooms, floor, size, rent, None, appartment_url, image_url, 
            provider.provider_string, None, move_in_date)
        print(appartment.appartment_url)
        app_list.append(appartment)
    return app_list

def getNumberFromString(st):
    return ''.join(map(str, [int(s) for s in st.split() if s.isdigit()]))

def fieldsAvailable(appart):
    li_fields = ["area", "address", "floor", "rent", "size"]
    for li_field in li_fields:
        if appart.find("li", {"class" : li_field}) == None:
            return False
    if appart.find("img", {"class": "img-responsive"}) == None:
        return False
    if appart.find("span", {"class": "date"}) == None:
        return False
    return True
    
    

def getFloor(f):
    if "BV" in f:
        return 0
    else:
        return getNumberFromString(f)