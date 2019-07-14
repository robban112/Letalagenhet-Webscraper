from lxml import html
import requests
from bs4 import BeautifulSoup
from enum import Enum
from WebScraper import scrapePages
from SollentunaParser import getAvailableAppartmentsFromSollentuna
from SigtunaHemParser import getAvailableAppartmentsFromSigtunaHem
from TelgeParser import getAvailableAppartmentsFromTelge
from Appartment import *

# Firebase stuff:
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Provider:
    def __init__(self, provider_string, request_url, appartment_url, location_index=None, 
    address_index=None, rooms_index=None, size_index=None, floor_index=None, rent_index=None, 
    available_until_index=None, number_of_signed_up=None, has_duplicates=False, pathToNextButton="//a[@class='btn next']",
    move_in_date=None):
        self.request_url = request_url
        self.appartment_url = appartment_url
        self.location_index = location_index
        self.address_index = address_index
        self.rooms_index = rooms_index
        self.floor_index = floor_index
        self.size_index = size_index
        self.rent_index = rent_index
        self.available_until_index = available_until_index
        self.number_of_signed_up = number_of_signed_up
        self.has_duplicates = has_duplicates
        self.pathToNextButton = pathToNextButton
        self.provider_string = provider_string
        self.move_in_date = move_in_date



FORVALTAREN_URL = 'https://www.forvaltaren.se/ledigt/lagenhet'
HASSELBY_HEM_URL = 'https://bostad.hasselbyhem.se/HSS/Object/object_list.aspx?cmguid=4e6e781e-5257-403e-b09d-7efc8edb0ac8&objectgroup=1'
SOLLENTUNA_HEM_URL = 'https://www.sollentunahem.se/ledigt-just-nu/lagenheter/GetObjects/'
VASBY_HEM_URL = 'https://www.vasbyhem.se/ledigt/sok/lagenhet'
HANINGE_BOSTADER_URL = 'https://minasidor.haningebostader.se/ledigt/sok/lagenhet'
IKANO_BOSTAD_URL = 'https://hyresratt.ikanobostad.se/ledigt/sok/lagenhet'
SIGTUNA_HEM_URL = 'https://sigtunahem.se/sok-ledigt/?pagination=1&paginationantal=1000'
TYRESO_BOSTADER_URL = 'https://www.tyresobostader.se/ledigt/lagenhet'
BOTKYRKA_BYGGEN_URL = 'https://www.botkyrkabyggen.se/ledigt/sok/lagenhet'
TELGE_URL = 'https://hyresborsen.telge.se/res/themes/telgebostader/pages/public/objectlistpublicb.aspx?objectgroup=1'

FORVALTAREN = Provider("Förvaltaren",FORVALTAREN_URL, 'https://www.forvaltaren.se/ledigt/', 0, 0, 1, 2, 3, 4, 5, 6, False)
HASSELBY_HEM = Provider("Hässelby Hem",HASSELBY_HEM_URL, 'https://bostad.hasselbyhem.se/HSS/Object/', 1, 0, 1, 2, None, 3, 4, 5, False)
SOLLENTUNA_HEM = Provider("Sollentuna Hem",SOLLENTUNA_HEM_URL, 'https://www.sollentunahem.se/ledigt/', 0, 1, 1, 2, 3, 4, 5, 6, True)
VASBY_HEM = Provider("Väsby Hem",VASBY_HEM_URL, 'https://www.vasbyhem.se/ledigt/detalj/', 1, 1, 2, 3, 4, 5, 6, 7, True)
HANINGE_BOSTADER = Provider("Haninge Bostäder",HANINGE_BOSTADER_URL, 'https://minasidor.haningebostader.se/ledigt/detalj/', 1, 0, 1, 2, None, 3, 4, 5, False)
IKANO_BOSTAD = Provider("Ikano Bostad",IKANO_BOSTAD_URL, 'https://hyresratt.ikanobostad.se/ledigt/detalj/', 1, 1, 2, 3, 0, 4, 5, None, False)
SIGTUNA_HEM = Provider("Sigtuna Hem", SIGTUNA_HEM_URL, 'https://sigtunahem.se/sok-ledigt/ledig-lagenhet/', pathToNextButton="//a[@href='https://sigtunahem.se/sok-ledigt/?pagination=3&paginationantal=10']")
TYRESO_BOSTADER = Provider("Tyresö Bostäder", TYRESO_BOSTADER_URL, 'https://www.tyresobostader.se/ledigt/detalj/', location_index=0, address_index=1, 
    rooms_index=1, size_index=2, floor_index=None, rent_index=3, available_until_index=4, number_of_signed_up=None, has_duplicates=False)
BOTKYRKA_BYGGEN = Provider("Botkyrka Byggen", BOTKYRKA_BYGGEN_URL, 'https://www.botkyrkabyggen.se/ledigt/detalj/', location_index=0, address_index=0, 
    rooms_index=1, size_index=2, floor_index=None, rent_index=3, available_until_index=4, number_of_signed_up=None, has_duplicates=False, move_in_date=5)
TELGE = Provider("Telge", TELGE_URL, "",location_index=0, address_index=1, rooms_index=1, size_index=2, floor_index=None, rent_index=3,available_until_index=None,number_of_signed_up=None, has_duplicates=False, move_in_date=None)

def getPageContent(provider):
    htmls = scrapePages(provider.request_url, provider.pathToNextButton)
    app_list = []
    for html in htmls:
        page_content = BeautifulSoup(html, "html.parser")
        app_list += getAvailableAppartmentsFrom(provider, page_content)
    return app_list

    
def getAvailableAppartmentsFrom(provider, page_content):
    if provider == SOLLENTUNA_HEM:
        return getAvailableAppartmentsFromSollentuna(page_content, provider)
    elif provider == SIGTUNA_HEM:
        return getAvailableAppartmentsFromSigtunaHem(page_content, provider)
    #elif provider == TELGE:
    #    return getAvailableAppartmentsFromTelge(page_content,provider)
    else:
        return getStandardizedAppartmentsList(page_content, provider)
        

def getStandardizedAppartmentsList(page_content, provider):
    appartments = page_content.find_all("tr")
    app_list = []
    for index, appart_html in enumerate(appartments):
        if index == 0 or (provider.has_duplicates and index % 2 == 0):
            continue
        app_list.append(getAppartment(appart_html, provider, index))
    return app_list

def getAppartment(appart_html, provider, index):
    spans = appart_html.find_all('span')
    a = appart_html.find_all('a')
    if len(spans) > 0 and len(a) > 0:
        location = spans[provider.location_index].text
        address = a[provider.address_index].text
        rooms = spans[provider.rooms_index].text
        floor = spans[provider.floor_index].text if provider.floor_index != None else 'null'
        size = spans[provider.size_index].text.replace(u'\xa0', '')
        rent = spans[provider.rent_index].text.replace(u'\xa0', '')
        available_until = spans[provider.available_until_index].text if provider.available_until_index != None else 'null'
        number_of_people_signed_up = spans[provider.number_of_signed_up].text if provider.number_of_signed_up != None else 'null'
        move_in_date = spans[provider.move_in_date].text if provider.move_in_date != None else 'null'

        appartment_url = getLink(a, provider)
        return Appartment(location, address, rooms, floor, size, rent, number_of_people_signed_up, 
            appartment_url, "", provider.provider_string,available_until,move_in_date)
        
    

def getLink(aelem, provider):
    return provider.appartment_url + aelem[provider.address_index]['href']

def dumpToDb(appartments):
    db = firestore.client()
    doc_ref = db.collection(u'appartments')
    for app in appartments:
        doc_ref.add(app.getJSON())    

def mainProgram():
    listOfAppProviders = [TELGE,BOTKYRKA_BYGGEN,TYRESO_BOSTADER,SIGTUNA_HEM,IKANO_BOSTAD,HANINGE_BOSTADER,VASBY_HEM,SOLLENTUNA_HEM,HASSELBY_HEM,FORVALTAREN]
    cred = credentials.Certificate('hyresbevakaren-firebase-adminsdk-oqc7z-e4bcd83e25.json')
    firebase_admin.initialize_app(cred)
    #
    app = list(filter(lambda x: x != None, getPageContent(TELGE))) # Run single 
    dumpToDb(app)
    #


    #for appProvider in listOfAppProviders:
    #    app = list(filter(lambda x: x != None, getPageContent(appProvider)))
    #    dumpToDb(app)
    #    for appart in app:
    #        print(appart.getJSON())
