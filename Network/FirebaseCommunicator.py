import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Model.Appartment import *

def dumpToDb(appartments, provider):
    db = firestore.client()
    provider_ref = db.collection(u'providers').document(provider.provider_string)
    app_ref = provider_ref.collection(u'appartments')

    for app in appartments:
        app_ref.add(app.getJSON())

def parseToAppartment(appartment):
    return Appartment(appartment['location'], appartment['address'], 
            appartment['rooms'], appartment['floor'], appartment['size'], appartment['rent'], 
            appartment['number_of_people_signed_up'], appartment['appartment_url'], 
            appartment['image_url'], appartment['provider'], appartment['available_until'],
            appartment['move_in_date'])

def appartmentExists(appartment, existing_appartments):
    _existing_appartments = existing_appartments
    for existing in _existing_appartments:
        
        existing_appartment = parseToAppartment(existing)
        if (getFieldHash(appartment) == getFieldHash(existing_appartment)):
            return True
    return False

def getOldAppartments(found_appartments, existing_appartments):
    old_appartments = []
    existing_appartments = map(lambda x: parseToAppartment(x), existing_appartments)
    copy = existing_appartments
    copy2 = found_appartments
    copy_list = list(map(lambda x: x.getJSON(),copy))
    copy2_list = list(map(lambda x: x.getJSON(), copy2))
    print("DEBUG2 : " + str(copy_list))
    print("\n\nDEBUG: " + str(copy2_list))
    for existing in existing_appartments:
        for found in found_appartments:
            if getFieldHash(found) == getFieldHash(existing):
                old_appartments.append(existing)
    return old_appartments

def getFieldHash(__appartment):
    field_hash = getFieldSafe(__appartment.location) + getFieldSafe(__appartment.address) + \
        getFieldSafe(__appartment.rooms) + getFieldSafe(__appartment.floor) + \
        getFieldSafe(__appartment.size) + getFieldSafe(__appartment.rent) + \
        getFieldSafe(__appartment.number_of_people_signed_up) + \
        getFieldSafe(__appartment.provider) + getFieldSafe(__appartment.available_until) + \
        getFieldSafe(__appartment.move_in_date) + getFieldSafe(__appartment.image_url)
    return field_hash

def getFieldSafe(field):
    if field == None:
        return ""
    return str(field)

#def archiveOldAppartments(appartments):

def getKey(appartment, doc):
    for d in doc:
        d_dict = d.to_dict()
        app = parseToAppartment(d_dict)
        if (getFieldHash(appartment) == getFieldHash(app)):
            return d.id
    print("ERROR: Couldn't find id for old appartment!")

def handleNewAppartments(newAppartments, provider):
    print("\nFound " + str(len(newAppartments)) + " new appartments for provider " + provider.provider_string+ "\n")
    print("\n------ UPLOADING: -------\n")
    print(list(map(lambda x: x.getJSON(), newAppartments)))
    print("\n------------------------\n")
    dumpToDb(newAppartments, provider)

def handleOldAppartments(oldAppartments, keysOldAppartments):
    print("\n------ ARCHIVING OLD APPARTMENTS: -------\n")
    print(list(map(lambda x: x.getJSON(), oldAppartments)))
    print("\n-----------------------------------------\n")

def updateDatabase(appartments, provider):
    db = firestore.client()
    provider_ref = db.collection(u'providers').document(provider.provider_string)
    app_ref = provider_ref.collection(u'appartments')
    doc = app_ref.get()
    list_doc = list(doc)
    app_dicts = None
    if len(list_doc) > 0:
        app_dicts = map(lambda x: x.to_dict(), list_doc)
        list_app_dicts = list(app_dicts)
        print("\n---- Appartments in database ----\n")
        print(list_app_dicts)
        print("\n---------------------------------\n")
        newAppartments = list(filter(lambda x: not appartmentExists(x, list_app_dicts), appartments))
        oldAppartments = getOldAppartments(appartments, list_app_dicts)
        keysOldAppartments = list(map(lambda x: getKey(x, doc), oldAppartments))
        handleOldAppartments(oldAppartments, keysOldAppartments)
    else: 
        print("\nProvider has no appartments\n")
        newAppartments = appartments

    if 'newAppartments' in locals() and len(newAppartments) > 0:
        handleNewAppartments(newAppartments, provider)
        
def main():
    cred = credentials.Certificate('hyresbevakaren-firebase-adminsdk-59i02-4c2efe1452.json')
    firebase_admin.initialize_app(cred)
    updateDatabase([])

#main()