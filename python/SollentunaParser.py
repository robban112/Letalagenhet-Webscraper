from bs4 import BeautifulSoup

def getAvailableAppartmentsFromSollentuna(page_content):
    app_dict = {}
    for index, appart in enumerate(page_content.find_all("article")):
        rent = appart.find("div", {"class": "c-objects__item__price"}).text
        item_info = appart.find("div", {"class": "c-objects__item__info"}).text
        address = appart.find("h1", {"class": "c-objects__item__heading"}).text
        (rooms, size, location) = getItemInfo(item_info)

def getItemInfo(info):
    infos = info.split('|')
    if len(infos) > 2:
        rooms = [int(s) for s in infos[0].split() if s.isdigit()][0]
        size = [int(s) for s in infos[1].split() if s.isdigit()][0]
        location = infos[2].strip()
        return (rooms, size, location)
print(getItemInfo("asd"))