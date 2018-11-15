from flask import Flask, jsonify, request, json
from app.controllers.helper import ParcelList
from app.models.parcel import Parcel


app = Flask(__name__)
parcel = ParcelList()


@app.route('/')
def index():
    return "<h2 style='text-align: center;'>Welcome to sendIT</h2>"


@app.route('/api/v1/parcels')
def get_parcels():
    
    """ Get all parcel delivery orders """

    return jsonify({ 'Parcels': parcel.get_all_parcels() }), 200


@app.route('/api/v1/parcels', methods=['POST'])
def add_parcels():

    """ Create a parcel delivery order """

    data = request.get_json()

    if not type(data) == dict:
        return jsonify({
            "message":'Data must be in dictionary format',
            "required format":{"userid": "int", "weight": "float",
                "status":"string","destination":"string","pickup":"string"}
            }), 400

    if 'userId' not in list(data.keys()):
        return jsonify({
            "message":'User Id missing in data',
            "required format":{"userid": "int", "weight": "float",
                "status":"string","destination":"string","pickup":"string"}
            }), 400

    
    if 'weight' not in list(data.keys()):
        return jsonify({
            "message":'Weight missing in data',
            "required format":{"userid": "int", "weight": "float",
                "status":"string","destination":"string","pickup":"string"}
            }), 400
            
    if 'status' not in list(data.keys()):
        return jsonify({
            "message":'Status missing in data',
            "required format":{"userid": "int", "weight": "float",
                "status":"string","destination":"string","pickup":"string"}
            }), 400

    if 'destination' not in list(data.keys()):
        return jsonify({
            "message":'Destination missing in data',
            "required format":{"userid": "int", "weight": "float",
                "status":"string","destination":"string","pickup":"string"}
            }), 400

    if 'pickup' not in list(data.keys()):
        return jsonify({
            "message":'Pickup missing in data',
            "required format":{"userid": "int", "weight": "float",
                "status":"string","destination":"string","pickup":"string"}
            }), 400

    parcel_id = 1+parcel.get_highest_parcel_id()
    new_parcel = parcel.add_parcel(parcel_id, data['userId'], data['weight'], data['pickup'], data['destination'], data['status'],)

    return jsonify({"Added Parcel":new_parcel}), 201


@app.route('/api/v1/parcels/<int:parcel_id>')
def get_parcel(parcel_id):

    """ Get a Parcel """

    if parcel.get_parcel(parcel_id):
        return jsonify({"Search":parcel.get_parcel(parcel_id)}), 200
    return jsonify({"message":"Parcel Not Found"}), 400


@app.route('/api/v1/users/<int:userId>/parcels')
def get_by_user(userId):

    """ Get Parcels by user """

    if parcel.get_parcel_user(userId):
        return jsonify({"Search":parcel.get_parcel_user(userId)}), 200
    return jsonify({"message":"User has no parcel delivery orders"}), 400


@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
def cancel_order(parcel_id):

    """ Cancel parcel order """

    if parcel.get_parcel(parcel_id):
        parcel.update_status(parcel_id)
        return jsonify({"Search":"Parcel delivery order has been cancelled"}), 200
    return jsonify({"message":"Parcel Not Found"}), 400


@app.errorhandler(405)
def no_method(error):
    return jsonify({'message':'Requested method not allowed, try a different method'}), 405


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found on server, check the url'}), 404
