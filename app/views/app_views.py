from flask import Flask, jsonify, request
from ..controllers.database import DatabaseConnection 
from ..controllers.auth import Auth 
from ..controllers.order import Orderz 
from ..models.app_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity
from flask_cors import CORS


db = DatabaseConnection()
auth = Auth()
order = Orderz()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'thisissecret'
jwt = JWTManager(app)



@app.route('/api/v1')
def index():
    
    return "<h2 style='text-align: center'>Welcome 2 Week 2</h2>"

@app.route('/auth/signup', methods=['POST'])
def add_user():

    data = request.get_json()
    return auth.signup(data)


@app.route('/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    return auth.login(data)

@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def add_order():
    data = request.get_json()
    return order.add_order( data)


@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def get_orders():

    return order.get_orders()


@app.route('/api/v1/parcels/<int:id>', methods=['GET'])
@jwt_required
def get_an_order(id):
    return order.get_order(id)


@app.route('/api/v1/parcels/<int:id>/destination', methods=['PUT'])
@jwt_required
def update_destination(id):
    
    data = request.get_json()
    return order.update_dest(id, data)

@app.route('/api/v1/parcels/<int:id>/status', methods=['PUT'])
@jwt_required
def update_status(id):
    
    data = request.get_json()
    return order.update_status(id, data)

@app.route('/api/v1/parcels/<int:parcel_id>/presentLocation', methods=['PUT'])
@jwt_required
def update_presentLocation(parcel_id):
    
    data = request.get_json()
    return order.update_present(parcel_id, data)

@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed, try a different method'}), 405

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found on server, check the url'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message':'internal server error, check the inputs'}), 500