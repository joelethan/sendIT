from flask import jsonify
from .database import DatabaseConnection 
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.app_models import User
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity


db = DatabaseConnection()


class Orderz:
    def add_order(self, current_user, data):

        """ Place a delivery order """
        validate = db.validate_data('weight', list(data.keys()))
        if validate:
            return validate

        validate = db.validate_data('pickup_location', list(data.keys()))
        if validate:
            return validate

        validate = db.validate_data('present_location', list(data.keys()))
        if validate:
            return validate

        validate = db.validate_data('destination', list(data.keys()))
        if validate:
            return validate


        weight = data['weight']
        pickup_location = data['pickup_location']
        present_location = data['present_location']
        destination = data['destination']


        if not type(weight) == float:
            return jsonify({'message':'Weight must be interger'}), 400
        if not type(pickup_location) == str:
            return jsonify({'message':'Pickup location must be String'}), 400
        if not type(present_location) == str:
            return jsonify({'message':'Present location must be String'}), 400
        if not type(destination) == str:
            return jsonify({'message':'Destination must be String'}), 400


        db.place_order(current_user['id'], weight, pickup_location, present_location, destination)
        return jsonify({'message' : 'Order recieved'}), 201

    def get_orders(self, current_user):
        if current_user['admin'] == True:
            orders = db.get_orders()
        else:
            """ by user """
            orders = db.get_user_orders(current_user['id'])

        if not orders:
            return jsonify({'Orders' : 'No orders found'}), 200

        return jsonify({'Orders' : orders}), 200

    def get_order(self, id, current_user):
        order = db.get_an_order('parcel_id', id)
        if not order:
            return jsonify({'message' : 'Parcel not found!!'}), 400

        if current_user['admin'] == True or current_user['id'] == order[2]:
            return jsonify({'Order' : order}), 200

        return jsonify({'message' : 'You only view Orders you placed'}), 400 

    def update_dest(self, parcel_id, current_user, data):
        order = db.get_an_order('parcel_id', parcel_id)
        if not order:
            return jsonify({'message' : 'Parcel not found!!'}), 400

        if current_user['id'] != db.get_user_id(parcel_id):
            return jsonify({'message' : 'You only view Orders you placed'}), 400

        validate = db.validate_data('destination', list(data.keys()))
        if validate:
            return validate

        destination = data['destination']
        if destination in db.get_item_from_parcels('destination', parcel_id):
            return  jsonify({'message':'Parcel destination is already {}'.format(destination)}), 400

        if not type(destination) == str:
            return jsonify({'message':'Destination must be String'}), 400
        if not destination.strip():
            return jsonify({'message':'Destination cannot be empty'}), 400

        db.update_destination(parcel_id, (destination).strip())
        return jsonify({'message' : 'Parcel destination Updated to \'{}\' '.format(destination)}), 200

    def update_status(self, parcel_id, current_user, data):
        order = db.get_an_order('parcel_id', parcel_id)
        if not order:
            return jsonify({'message' : 'Parcel not found!!'}), 400
        if current_user['admin'] != True:
            return jsonify({'message':'You are not authorised to perform this action!!!!'}), 403


        validate = db.validate_data('status', list(data.keys()))
        if validate:
            return validate

        status = data['status']

        if status in db.get_item_from_parcels('status', parcel_id):
            return  jsonify({'message':'Parcel status is already \'{}\' '.format(status)}), 400

        if not type(status) == str:
            return jsonify({'message':'Status must be String'}), 400
        if not status.strip():
            return jsonify({'message':'Status cannot be empty'}), 400
        if not status.title() in ['New','Transportation','Cancelled','Delivered']:
            return jsonify({'message':"Status must be in the given list: ['New','Transportation','Cancelled','Delivered']"})

        db.update_status(parcel_id, (status).strip().title())
        return jsonify({'message' : 'Parcel status Updated to {}'.format(status.title())}), 200

    def update_present(self, parcel_id, current_user, data):
        order = db.get_an_order('parcel_id', parcel_id)
        if not order:
            return jsonify({'message' : 'Parcel not found!!'}), 400

        if current_user['admin'] != True:
            return jsonify({'message':'You are not authorised to perform this action!!!!'}), 403


        validate = db.validate_data('present_location', list(data.keys()))
        if validate:
            return validate

        location = data['present_location']

        if location in db.get_item_from_parcels('present_location', parcel_id):
            return  jsonify({'message':'Parcel location is already \'{}\' '.format(location)}), 400

        if not type(location) == str:
            return jsonify({'message':'Location must be String'}), 400
        if not location.strip():
            return jsonify({'message':'Location cannot be empty'}), 400

        db.update_presentLocation(parcel_id, (location).strip())
        return jsonify({'message' : 'Parcel present location Updated to \'{}\' '.format(location)}), 200