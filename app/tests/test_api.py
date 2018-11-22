import json
from unittest import TestCase
from ..controllers.database import DatabaseConnection 
from ..views.app_views import db,app


class APITestCase(TestCase):
    def setUp(self):
        
        self.client = app.test_client()
        self.user_signUp = {"username": "joelethan","email": "joelethan@gm",
                                "password": "password"}
        self.user_login = {"username": "joelethan","password": "password"}
        self.user2_signUp = {"username": "joelethan2","email": "joelethan2@gm",
                                "password": "password"}
        self.user2_login = {"username": "joelethan2","password": "password"}
        self.parcel = {"weight": 2.3,"pickup_location":"From",
                            "present_location":"Home","destination":"To"}

        db.create_tables()

    def tearDown(self):
        db.drop_tables()


    def test_index(self):
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('joelethan', json.loads(response.data)['message'])

    def test_signin(self):
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 200)
        
    def test_add_parcel_by_user(self):
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        self.assertEqual(login_resp.status_code, 200)
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 201)
        
    def test_add_parcel_by_admin(self):
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertIn('You don\'t have access to this function!', json.loads(response1.data)['message'])
        self.assertEqual(response1.status_code, 403)


    def test_signup_no_username(self):
        del self.user_signUp['username']
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('username field must be present', json.loads(response.data)['message'])


    def test_signup_username_type(self):
        self.user_signUp['username'] = 7
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username must be string', json.loads(response.data)['message'])


    def test_signup_empty_username(self):
        self.user_signUp['username'] = '  '
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username cannot be empty', json.loads(response.data)['message']) 


    def test_signup_short_username(self):
        self.user_signUp['username'] = '  ff'
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username too short', json.loads(response.data)['message']) 


    def test_signup_no_email(self):
        del self.user_signUp['email']
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email field must be present', json.loads(response.data)['message'])


    def test_signup_empty_email(self):
        self.user_signUp['email'] = '  '
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email cannot be empty', json.loads(response.data)['message'])


    def test_signup_email_type(self):
        self.user_signUp['email'] = ['t']
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email must be string', json.loads(response.data)['message'])


    def test_signup_email_format(self):
        self.user_signUp['email'] = 't'
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email format', json.loads(response.data)['message']) 


    def test_signup_no_password(self):
        del self.user_signUp['password']
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password field must be present', json.loads(response.data)['message'])


    def test_signup_password_type(self):
        self.user_signUp['password'] = 8
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password must be string', json.loads(response.data)['message'])


    def test_signup_empty_password(self):
        self.user_signUp['password'] = '  '
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password cannot be empty', json.loads(response.data)['message'])


    def test_signup_short_password(self):
        self.user_signUp['password'] = '  pass'
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password too short', json.loads(response.data)['message']) 


    def test_signin_no_username(self):
        del self.user_login['username']
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 400)
        self.assertIn('username field must be present', json.loads(login_resp.data)['message'])


    def test_signin_username_type(self):
        self.user_login['username'] = 9
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 400)
        self.assertIn('Username must be string', json.loads(login_resp.data)['message']) 


    def test_signin_no_password(self):
        del self.user_login['password']
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 400)
        self.assertIn('password field must be present', json.loads(login_resp.data)['message']) 


    def test_signin_password_type(self):
        self.user_login['password'] = 9
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 400)
        self.assertIn('Password must be string', json.loads(login_resp.data)['message']) 


    def test_signin_wrong_username(self):
        self.user_login['username'] = 'simon'
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 401)
        self.assertIn('Could not verify User', json.loads(login_resp.data)['message']) 


    def test_signin_wrong_password(self):
        self.user_login['password'] = 'simon'
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 401)
        self.assertIn('Could not verify User', json.loads(login_resp.data)['message'])
        
        
    def test_parcels_no_weight(self):
        del self.parcel['weight']
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('weight field must be present', json.loads(response1.data)['message']) 
        
        
    def test_parcels_weight_type(self):
        self.parcel['weight'] = 4
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('Weight must be interger', json.loads(response1.data)['message']) 
        
        
    def test_parcels_no_pickup(self):
        del self.parcel['pickup_location']
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('pickup_location field must be present', json.loads(response1.data)['message'])
        
        
    def test_parcels_pickup_type(self):
        self.parcel['pickup_location'] = 6
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('Pickup location must be String', json.loads(response1.data)['message']) 
        
        
    def test_parcels_no_location(self):
        del self.parcel['present_location']
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('present_location field must be present', json.loads(response1.data)['message'])
        
        
    def test_parcels_location_type(self):
        self.parcel['present_location'] = 6
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('Present location must be String', json.loads(response1.data)['message']) 
        
        
    def test_parcels_no_destination(self):
        del self.parcel['destination']
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('destination field must be present', json.loads(response1.data)['message'])
        
        
    def test_parcels_destination_type(self):
        self.parcel['destination'] = 8
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.parcel)
            )
        self.assertEqual(response1.status_code, 400) 
        self.assertIn('Destination must be String', json.loads(response1.data)['message']) 


    def test_get_parcels_by_admin(self):
        self.parcel['destination'] = 8
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.get(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'
            )
        self.assertEqual(response1.status_code, 200) 
        
        
    def test_get_parcels_by_user(self):
        self.parcel['destination'] = 8
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.client.post('/auth/signup', data=json.dumps(self.user2_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user2_login), 
                            content_type='application/json')
        access_token = json.loads(login_resp.data.decode())
        response1 = self.client.get(
            '/api/v1/parcels',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'
            )
        self.assertEqual(response1.status_code, 200)