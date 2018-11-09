class Parcel():
    def __init__(self, parcel_id, weight, status):
        self.parcel_id = parcel_id
        self.weight = weight
        self.status = status

    def parcel_input(self):
        data = {"parcel_id": self.parcel_id, "weight": self.weight, "status":self.status}
        return data

class ParcelList():

    def __init__(self):
        self.parcel_list = []# {'parcel_id':1, 'weight': 5,'status':'pending'},{'parcel_id':2, 'weight': 2,'status':'pending'},{'parcel_id':3, 'weight': 2,'status':'pending'},{'parcel_id':4, 'weight': 2,'status':'pending'},{'parcel_id':5, 'weight': 2,'status':'pending'}]

    def add_parcel(self, parcel_id, weight, status):
        if not type(weight) == int:
            return 'quantity must be an Integer!!'
            
        if not type(parcel_id) == int:
            return 'parcel_id must be an Integer!!'

        if not type(status) == str:
            return 'status must be a string!!'

        if not status.strip():
            return 'status cannot be empty!'

        parcel = Parcel(parcel_id, weight, status).parcel_input()
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
