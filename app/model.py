from app.valid import Validate

validate = Validate()
class Parcel():
    def __init__(self, parcel_id, weight, status, pickup, destination):
        self.parcel_id = parcel_id
        self.weight = weight
        self.status = status
        self.destination = destination
        self.pickup = pickup

    def parcel_input(self):
        data = {"parcel_id": self.parcel_id, "weight": self.weight, "pickup-location":self.pickup, 
                "destination": self.destination, "status":self.status}
        return data

class ParcelList():

    def __init__(self):
        self.parcel_list = []# {'parcel_id':1, 'weight': 5,'status':'pending'},{'parcel_id':2, 'weight': 2,'status':'pending'},{'parcel_id':3, 'weight': 2,'status':'pending'},{'parcel_id':4, 'weight': 2,'status':'pending'},{'parcel_id':5, 'weight': 2,'status':'pending'}]

    def add_parcel(self, parcel_id, weight, pickup, destination, status):

        # validate.field_type(weight, float)

        if not type(weight) == float:
            return 'weight must be an Float!!'
            
        if not type(parcel_id) == int:
            return 'parcel_id must be an Integer!!'

        # if not type(status) in [str]:
        #     return 'status must be an String!!'

        # if not type(destination) == str:
        #     return 'destination must be a string!!'

        # if not type(pickup) == str:
        #     return 'pickup must be a string!!'

        if not status.strip():
            return 'status cannot be empty!'

        if not pickup.strip():
            return 'pickup cannot be empty!'

        if not destination.strip():
            return 'destination cannot be empty!'

        parcel = Parcel(parcel_id, weight, pickup, destination, status).parcel_input()
        self.parcel_list.append(parcel)
        return parcel

    def update_status(self, parcel_id, status):
        for parcel in self.parcel_list:
            if parcel['parcel_id']==parcel_id: 
                parcel['status']=status
                return parcel

    def get_all_parcels(self):
        return self.parcel_list

    def get_parcel(self, parcel_id):
        for parcel in self.parcel_list:
            if parcel['parcel_id']==parcel_id:
                return parcel

    def get_highest_parcel_id(self):
        id_list=[]
        if self.parcel_list:
            for parcel in self.parcel_list:
                id_list.append(parcel['parcel_id'])
            return(max(id_list))
        return 0
