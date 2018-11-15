class Parcel():
    def __init__(self, parcel_id, userId, weight, pickup, destination, status):
        self.parcel_id = parcel_id
        self.weight = weight
        self.userId = userId
        self.status = status
        self.destination = destination
        self.pickup = pickup

    def parcel_input(self):
        data = {"parcel_id": self.parcel_id, "userId":self.userId, "weight": self.weight, "pickup-location":self.pickup, 
                "destination": self.destination, "status":self.status}
        return data