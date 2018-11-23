from flask import jsonify
from .database import DatabaseConnection 
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.app_models import User
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity


db = DatabaseConnection()


class Auth:
    def signup(self, data):
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
            return jsonify({'message':'User already exists'}), 400

        if db.get_user('email', email):
            return jsonify({'message':'Your email address is already registered'}), 400


        password = generate_password_hash(password)

        db.add_user((username).strip(), (email).strip(), password)
        db.auto_admin()
        return jsonify({'message':'User {} registered'.format(username)}), 201

    def login(self, data):
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
            return jsonify({'token': access_token, 'message':'Login successful'}), 200


        return jsonify({'message':'Could not verify User'}), 401
