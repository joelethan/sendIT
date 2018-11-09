from flask import Flask, jsonify, request, json
from app.model import ParcelList, Parcel

app = Flask(__name__)
parcel = ParcelList() 


@app.route('/')
def index():
    return "<h2 style='text-align: center;'>Welcome to sendIT</h2>"


@app.route('/api/v1/parcels', methods=['GET','POST'])
def get_parcels():
    if request.method == 'GET':
        return jsonify({ 'Parcels': parcel.get_all_parcels() }), 200
    else:
        data = request.get_json()
        
        if 'weight' not in list(data.keys()):
            return jsonify({
                "message":'Weight missing in data',
                "required format":{"weight": "int","status":"string"}
                }), 400
                
        if 'status' not in list(data.keys()):
            return jsonify({
                "message":'Status missing in data',
                "required format":{"weight": "int","status":"string"}
                }), 400

        parcel_id = 1+parcel.get_highest_parcel_id()
        new_parcel = parcel.add_parcel(parcel_id,  data['weight'], data['status'])

        if isinstance(new_parcel, str):
            return jsonify({"message":new_parcel}), 400

        return jsonify({"Added Parcel":new_parcel}), 201


@app.route('/api/v1/parcels/<int:parcel_id>', methods=['DELETE','GET','PUT'])
def get_parcel(parcel_id):
    if request.method == 'GET':
        # Get a Parcel
        if parcel.get_parcel(parcel_id):
            return jsonify({"Search":parcel.get_parcel(parcel_id)}), 200
        return jsonify("Parcel Not Found"), 400

    else: 
        # Update status
        data = request.get_json()
        if parcel.get_parcel(parcel_id):
            return jsonify({"Search":parcel.update_status(parcel_id, data['status'])}), 200
        return jsonify("Parcel Not Found"), 400


@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed, try a different method'}), 405

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found on server, check the url'}), 404
