from flask import Flask, jsonify, request
from ..controllers.database import DatabaseConnection 
from ..models.app_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger, swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity


db = DatabaseConnection()


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'thisissecret'
jwt = JWTManager(app)

Swagger(app)


@app.route('/api/v1/')
def index():
    return "<h2 style='text-align: center'>Welcome 2 Week 2</h2>"

@app.route('/auth/signup', methods=['POST'])
@swag_from('../Docs/signup.yml')
def add_user():

    data = request.get_json()
    validate = db.validate_data('username', list(data.keys()))
    if validate:
        return validate

    validate = db.validate_data('email', list(data.keys()))
    if validate:
        return validate

    validate = db.validate_data('password', list(data.keys()))
    if validate:
        return validate

    username = data['username']
    email = data['email']
    password = data['password']

    if not type(username) == str:
        return jsonify({'message':'Username must be string'}), 400
    username=(username).strip()

    if not type(email) == str:
        return jsonify({'message':'email must be string'}), 400
    email = (email).strip()

    if not type(password) == str:
        return jsonify({'message':'password must be string'}), 400
    password = (password).strip()

    if not username.strip():
        return jsonify({'message':'Username cannot be empty'}), 400

    if not email.strip():
        return jsonify({'message':'email cannot be empty'}), 400

    if not password.strip():
        return jsonify({'message':'password cannot be empty'}), 400

    if len(username)<3:
        return jsonify({'message':'Username too short, should have atleast 3 character'}), 400

    if len(password)<5:
        return jsonify({'message':'Password too short, should have atleast 5 character'}), 400

    if not '@' in email:
        return jsonify({'message':'Invalid email format'}), 400

    if db.get_user('username', username):
        return jsonify({'message':'Username already taken'}), 400

    if db.get_user('email', email):
        return jsonify({'message':'Your email address is already registered'}), 400


    password = generate_password_hash(password)

    db.add_user((username).strip(), (email).strip(), password)
    db.auto_admin()
    return jsonify({'message':'User {} registered'.format(username)}), 201

@app.route('/auth/login', methods=['POST'])
@swag_from('../Docs/signin.yml')
def login():

    data = request.get_json()

    validate = db.validate_data('username', list(data.keys()))
    if validate:
        return validate

    validate = db.validate_data('password', list(data.keys()))
    if validate:
        return validate

    req_username = data['username']
    req_password = data['password']

    if not type(req_username) == str:
        return jsonify({'message':'Username must be string'}), 400
    req_username=(req_username).strip()

    if not type(req_password) == str:
        return jsonify({'message':'Password must be string'}), 400
    req_password=(req_password).strip()


    db_user = db.get_user('username', req_username)

    if not db_user:
        return jsonify({'message':'Could not verify User'}), 401

    user = User(db_user[0], db_user[1], db_user[2], db_user[3], db_user[4])

    if user.username == req_username and check_password_hash( user.password, req_password):
        access_token = create_access_token(dict(user=req_username,admin=db_user[4],id=db_user[0]))
        return jsonify({'token': access_token, 'message':'{} has logged-in'.format(user.username)}), 200


    return jsonify({'message':'Could not verify User'}), 401

@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def add_order():
    current_user = get_jwt_identity()
    if current_user['admin'] != False:
        return jsonify({'message':'You don\'t have access to this function!!!!'}), 403

    """ Place a delivery order """

    data = request.get_json()

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


@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def get_orders():
    """ by Admin """
    current_user = get_jwt_identity()
    if current_user['admin'] == True:
        orders = db.get_orders()
    else:
        """ by user """
        orders = db.get_user_orders(current_user['id'])

    return jsonify({'Orders' : orders}), 200


@app.route('/api/v1/parcels/<int:id>', methods=['GET'])
@jwt_required
def get_an_order(id):
    current_user = get_jwt_identity()
    order = db.get_an_order('parcel_id', id)
    if not order:
        return jsonify({'msg' : 'Parcel not found!!'}), 400

    if current_user['admin'] == True or current_user['id'] == order[2]:
        return jsonify({'Order' : order}), 200

    return jsonify({'msg' : 'You only view Orders you placed'}), 400


@app.route('/api/v1/parcels/<int:id>/destination', methods=['PUT'])
@jwt_required
def update_destination(id):

    current_user = get_jwt_identity()
    if current_user['id'] != db.get_user_id(id):
        return jsonify({'msg' : 'You only view Orders you placed'}), 400

    data = request.get_json()

    validate = db.validate_data('destination', list(data.keys()))
    if validate:
        return validate

    destination = data['destination']

    if not type(destination) == str:
        return jsonify({'message':'Destination must be String'}), 400
    if not destination.strip():
        return jsonify({'message':'Destination cannot be empty'}), 400

    db.update_destination(id, (destination).strip())
    return jsonify({'message' : 'Parcel destination Updated to: {}'.format(destination)}), 202


@app.route('/api/v1/parcels/<int:id>/status', methods=['PUT'])
@jwt_required
def update_status(id):

    current_user = get_jwt_identity()
    if current_user['admin'] != True:
        return jsonify({'message':'You don\'t have access to this route!!!!'}), 403

    data = request.get_json()

    validate = db.validate_data('status', list(data.keys()))
    if validate:
        return validate

    status = data['status']

    if not type(status) == str:
        return jsonify({'message':'Status must be String'}), 400
    if not status.strip():
        return jsonify({'message':'Status cannot be empty'}), 400
    if not status.title() in ['New','Transportation','Cancelled','Delivered']:
        return jsonify({'message':"Status must be in the given list: ['New','Transportation','Cancelled','Complete']"})

    db.update_status(id, (status).strip().title())
    return jsonify({'message' : 'Parcel status Updated to: {}'.format(status.title())}), 202


@app.route('/api/v1/parcels/<int:id>/presentLocation', methods=['PUT'])
@jwt_required
def update_presentLocation(id):

    current_user = get_jwt_identity()
    if current_user['admin'] != True:
        return jsonify({'message':'You don\'t have access to this route!!!!'}), 403

    data = request.get_json()

    validate = db.validate_data('present_location', list(data.keys()))
    if validate:
        return validate

    location = data['present_location']

    if not type(location) == str:
        return jsonify({'message':'Location must be String'}), 400
    if not location.strip():
        return jsonify({'message':'Location cannot be empty'}), 400

    db.update_presentLocation(id, (location).strip())
    return jsonify({'message' : 'Parcel present location Updated to: {}'.format(location)}), 202


@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed, try a different method'}), 405

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found on server, check the url'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message':'internal server error, check the inputs'}), 500