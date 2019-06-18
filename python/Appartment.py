class Appartment:
    def __init__(self, location, address, rooms, floor, size, rent, number_of_people_signed_up, 
    appartment_url , image_url, provider, available_until):
        self.location = location
        self.address = address
        self.rooms = rooms
        self.floor = floor
        self.size = size
        self.rent = rent
        self.number_of_people_signed_up = number_of_people_signed_up
        self.image_url = image_url
        self.provider = provider
        self.appartment_url = appartment_url
        self.available_until = available_until

    def getJSON(self):
        return {
            "location" : self.location, "address" : self.address, "rooms" : self.rooms, 
            "floor" : self.floor, "size" : self.size, "rent" : self.rent, "provider": self.provider, 
            "appartment_url": self.appartment_url, "available_until" : self.available_until, 
            "number_of_people_signed_up" : self.number_of_people_signed_up
        }