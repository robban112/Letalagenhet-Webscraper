import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Appartment import *

def dumpToDb(appartments):
    db = firestore.client()
    doc_ref = db.collection(u'appartments')
    for app in appartments:
        doc_ref.add(app.getJSON())

def appartmentExists(appartment, existing_appartments):

    for existing in existing_appartments:
        existing_appartment = Appartment(existing['location'], existing['address'], 
            existing['rooms'], existing['floor'], existing['size'], existing['rent'], 
            existing['number_of_people_signed_up'], existing['appartment_url'], 
            existing['image_url'], existing['provider'], existing['available_until'],
            existing['move_in_date'])
        
        if (getFieldHash(appartment) == getFieldHash(existing_appartment)):
            return True
    print("not equal!")
    print(appartment.getJSON())
    print("\nexisting:\n")
    print((existing_appartments))
    print("\n")
    return False

def getFieldHash(appartment):
    field_hash = getFieldSafe(appartment.location) + getFieldSafe(appartment.address) + \
        getFieldSafe(appartment.rooms) + getFieldSafe(appartment.floor) + \
        getFieldSafe(appartment.size) + getFieldSafe(appartment.rent) + \
        getFieldSafe(appartment.number_of_people_signed_up) + \
        getFieldSafe(appartment.provider) + getFieldSafe(appartment.available_until) + \
        getFieldSafe(appartment.move_in_date)
    return field_hash

def getFieldSafe(field):
    if field == None:
        return ""
    return str(field)

def updateDatabase(appartments):
    db = firestore.client()
    doc_ref = db.collection(u'appartments')
    doc = doc_ref.get()
    app_dicts = map(lambda x: x.to_dict(), doc)
    newAppartments = list(filter(lambda x: not appartmentExists(x, list(app_dicts)), appartments))
    print("\nFound " + str(len(newAppartments)) + " new appartments\n")
    print("\n------ UPLOADING: -------\n")
    print(list(map(lambda x: x.getJSON(), newAppartments)))
    print("\n------------------------\n")
    #dumpToDb(newAppartments)


def main():
    cred = credentials.Certificate('hyresbevakaren-firebase-adminsdk-59i02-4c2efe1452.json')
    firebase_admin.initialize_app(cred)
    updateDatabase([])

#main()