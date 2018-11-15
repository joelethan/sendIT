from app.models.parcel import Parcel


class ParcelList():

    def __init__(self):
        self.parcel_list = []

    def add_parcel(self, parcel_id, userId, weight, pickup, destination, status):

        if not type(parcel_id) == int:
            return 'parcel_id must be an Integer!!'

        if not type(userId) == int:
            return 'userId must be an Integer!!'

        if not type(weight) == float:
            return 'weight must be an Float!!'

        if not type(pickup) == str:
            return 'pickup must be a string!!'

        if not type(destination) == str:
            return 'destination must be a string!!'

        if not type(status) == str:
            return 'status must be an String!!'

        if not pickup.strip():
            return 'pickup cannot be empty!'

        if not destination.strip():
            return 'destination cannot be empty!'

        if not status.strip():
            return 'status cannot be empty!'

        parcel = Parcel(parcel_id, userId, weight, pickup, destination, status).parcel_input()
        self.parcel_list.append(parcel)
        return parcel

    def update_status(self, parcel_id):
        for parcel in self.parcel_list:
            if parcel['parcel_id']==parcel_id: 
                parcel['status']='Cancelled'
                return parcel

    def get_all_parcels(self):
        return self.parcel_list

    def get_parcel(self, parcel_id):
        for parcel in self.parcel_list:
            if parcel['parcel_id']==parcel_id:
                return parcel

    def get_parcel_user(self, userId):
        ttt = []
        for parcel in self.parcel_list:
            if parcel['userId']==userId:
                ttt.append(parcel)
        return ttt

    def get_highest_parcel_id(self):
        id_list=[]
        if self.parcel_list:
            for parcel in self.parcel_list:
                id_list.append(parcel['parcel_id'])
            return(max(id_list))
        return 0
