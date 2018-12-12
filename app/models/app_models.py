class User():
    def __init__(self, user_id, username, email, password, admin):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

class ParcelOrder():
    def __init__(self, parcel_id, user_id, pickup_location, present_location, destination, status):
        self.parcel_id = parcel_id
        self.user_id = user_id
        self.pickup_location = pickup_location
        self.present_location = present_location
        self.destination = destination
        self.status = status