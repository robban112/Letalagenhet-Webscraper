# coding=utf-8
from lxml import html
import requests
import asyncio

from bs4 import BeautifulSoup
from enum import Enum
from WebScraper import *
from SollentunaParser import getAvailableAppartmentsFromSollentuna
from SigtunaHemParser import getAvailableAppartmentsFromSigtunaHem
from TelgeParser import getAvailableAppartmentsFromTelge
from Appartment import *
from Provider import Provider, ProviderIndexes

,import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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


#     (provider_string, request_url, appartment_url, location_index=None, 
#     address_index=None, rooms_index=None, size_index=None, floor_index=None, rent_index=None, 
#     available_until_index=None, number_of_signed_up=None, has_duplicates=False, pathToNextButton="//a[@class='btn next']",
#     move_in_date=None, image_index=0)

#FORVALTAREN = Provider("Förvaltaren",FORVALTAREN_URL, 'https://www.forvaltaren.se/ledigt/sok/lagenhet', 0, 0, 1, 2, 3, 4, 5, 6, False)
FORVALTAREN_INDEXES = ProviderIndexes(location_index=0, address_index=0, rooms_index=1, size_index=2, floor_index=3, rent_index=4,
    available_until_index=5, number_of_signed_up_index=6, image_index=2)
FORVALTAREN = Provider("Förvaltaren", FORVALTAREN_URL, 'https://www.forvaltaren.se/ledigt/', provider_indexes=FORVALTAREN_INDEXES, 
    has_duplicates=False, pathToNextButton=None, move_in_date=None, image_prepend_url='https://forvaltaren.se')


HASSELBY_HEM_INDEXES = ProviderIndexes(location_index=1, address_index=0, rooms_index=1, size_index=2, floor_index=None, rent_index=3,
    available_until_index=4, number_of_signed_up_index=5, image_index=0)
HASSELBY_HEM = Provider("Hässelby Hem",HASSELBY_HEM_URL, 'https://bostad.hasselbyhem.se/HSS/Object/', provider_indexes=HASSELBY_HEM_INDEXES, has_duplicates=False)

SOLLENTUNA_HEM_INDEXES = ProviderIndexes(location_index=0, address_index=1, rooms_index=1, size_index=2, floor_index=3, rent_index=4,
    available_until_index=5, number_of_signed_up_index=6, image_index=0)
SOLLENTUNA_HEM = Provider("Sollentuna Hem",SOLLENTUNA_HEM_URL, 'https://www.sollentunahem.se/ledigt/', provider_indexes=SOLLENTUNA_HEM_INDEXES,has_duplicates=True
    , pathToNextButton=None, move_in_date=None)

VASBY_HEM_INDEXES = ProviderIndexes(location_index=1, address_index=1, rooms_index=2, size_index=3, floor_index=4, rent_index=5,
    available_until_index=6, number_of_signed_up_index=7, image_index=0)
VASBY_HEM = Provider("Väsby Hem",VASBY_HEM_URL, 'https://www.vasbyhem.se/ledigt/detalj/', provider_indexes=VASBY_HEM_INDEXES, has_duplicates=True, 
    pathToNextButton=None, move_in_date=None)

HANINGE_BOSTADER_INDEXES = ProviderIndexes(location_index=1, address_index=0, rooms_index=1, size_index=2, floor_index=None, rent_index=3,
    available_until_index=4, number_of_signed_up_index=5, image_index=0)
HANINGE_BOSTADER = Provider("Haninge Bostäder",HANINGE_BOSTADER_URL, 'https://minasidor.haningebostader.se/ledigt/detalj/', provider_indexes= HANINGE_BOSTADER_INDEXES
    ,has_duplicates=False)

IKANO_BOSTAD_INDEXES = ProviderIndexes(location_index=1, address_index=1, rooms_index=2, size_index=3, floor_index=0, rent_index=4,
    available_until_index=5, number_of_signed_up_index=None, image_index=0)
IKANO_BOSTAD = Provider("Ikano Bostad",IKANO_BOSTAD_URL, 'https://hyresratt.ikanobostad.se/ledigt/detalj/', provider_indexes=IKANO_BOSTAD_INDEXES,
    has_duplicates=False)

SIGTUNA_HEM = Provider("Sigtuna Hem", SIGTUNA_HEM_URL, 'https://sigtunahem.se/sok-ledigt/ledig-lagenhet/', pathToNextButton="//a[@href='https://sigtunahem.se/sok-ledigt/?pagination=3&paginationantal=10']")

TYRESO_BOSTADER_INDEXES = ProviderIndexes(location_index=0, address_index=1, rooms_index=1, size_index=2, floor_index=None, rent_index=3, 
    available_until_index=4, number_of_signed_up_index=None, image_index=0)
TYRESO_BOSTADER = Provider("Tyresö Bostäder", TYRESO_BOSTADER_URL, 'https://www.tyresobostader.se/ledigt/detalj/', provider_indexes=TYRESO_BOSTADER_INDEXES,
     has_duplicates=False)

BOTKYRKA_BYGGEN_INDEXES = ProviderIndexes(location_index=0, address_index=0, rooms_index=1, size_index=2, floor_index=None, rent_index=3, 
    available_until_index=4, number_of_signed_up_index=None, image_index=1)
BOTKYRKA_BYGGEN = Provider("Botkyrka Byggen", BOTKYRKA_BYGGEN_URL, 'https://www.botkyrkabyggen.se/ledigt/detalj/', provider_indexes=BOTKYRKA_BYGGEN_INDEXES, 
    has_duplicates=False, move_in_date=5, image_prepend_url='https://botkyrkabyggen.se')

TELGE_INDEXES = ProviderIndexes(location_index=0, address_index=1, rooms_index=1, size_index=2, floor_index=None, rent_index=3,
    available_until_index=None,number_of_signed_up_index=None, image_index=2)
TELGE = Provider("Telge", TELGE_URL, "https://hyresborsen.telge.se/res/themes/telgebostader/pages/public/",provider_indexes=TELGE_INDEXES, 
    has_duplicates=False, move_in_date=None, image_prepend_url='https://hyresborsen.telge.se')

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
    # elif provider == TELGE:
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
        location = spans[provider.provider_indexes.location_index].text
        address = a[provider.provider_indexes.address_index].text
        rooms = spans[provider.provider_indexes.rooms_index].text
        floor = spans[provider.provider_indexes.floor_index].text if provider.provider_indexes.floor_index != None else 'null'
        size = spans[provider.provider_indexes.size_index].text.replace(u'\xa0', '')
        rent = spans[provider.provider_indexes.rent_index].text.replace(u'\xa0', '')
        available_until = spans[provider.provider_indexes.available_until_index].text if provider.provider_indexes.available_until_index != None else 'null'
        number_of_people_signed_up = spans[provider.provider_indexes.number_of_signed_up_index].text if provider.provider_indexes.number_of_signed_up_index != None else 'null'
        move_in_date = spans[provider.move_in_date].text if provider.move_in_date != None else 'null'
        appartment_url = getLink(a, provider)
        image_url = getAppartmentImage(provider, appartment_url)
        return Appartment(location, address, rooms, floor, size, rent, number_of_people_signed_up, 
            appartment_url, image_url, provider.provider_string,available_until,move_in_date)

## Retrieves the first image on detail page. This might not work for every provider!!
def getAppartmentImage(provider, appartment_url):
    if provider.image_prepend_url != None:
        html = BeautifulSoup(getHTML(appartment_url), "html.parser")
        imgs = html.find_all('img')
        if provider.provider_indexes.image_index >= len(imgs):
            return
        if len(imgs) > 0:
            imgurl = provider.image_prepend_url + str(imgs[provider.provider_indexes.image_index]['src'])
            print("IMAGE: " + imgurl)
            return imgurl
    

def getLink(aelem, provider):
    return provider.appartment_url + aelem[provider.provider_indexes.address_index]['href']

def dumpToDb(appartments):
    db = firestore.client()
    doc_ref = db.collection(u'appartments')
    for app in appartments:
        doc_ref.add(app.getJSON())    

def main(provider):
    print('Started to fetch: ' + provider.provider_string)
    appContent = getPageContent(provider)
    app = list(filter(lambda x: x != None, appContent))
    dumpToDb(app)
    for appart in app:
        print(appart.getJSON())
    print('Done fetching: ' + provider.provider_string)
    
def mainProgram():
    listOfAppProviders = [TELGE,BOTKYRKA_BYGGEN,TYRESO_BOSTADER,SIGTUNA_HEM,IKANO_BOSTAD,HANINGE_BOSTADER,VASBY_HEM,SOLLENTUNA_HEM,HASSELBY_HEM,FORVALTAREN]
    listOfAppProviders = [TELGE]
    cred = credentials.Certificate('hyresbevakaren-firebase-adminsdk-59i02-620a8327a5.json')
    firebase_admin.initialize_app(cred)
    
    loop = asyncio.get_event_loop()
    tasks = []
    main(BOTKYRKA_BYGGEN)
    # for appProvider in listOfAppProviders:
    #     tasks.append(asyncio.ensure_future(main(appProvider)))
    
    # loop.run_until_complete(asyncio.wait(tasks))

    #for appProvider in listOfAppProviders:
    #    task = asyncio.ensure_future(main(appProvider))
    #    #task = loop.create_task(main(appProvider))
    #    loop.run_until_complete(asyncio.gather(task))
