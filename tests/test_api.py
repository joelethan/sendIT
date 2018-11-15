import json
import unittest
from app.controllers.helper import ParcelList

from app.views.api_views import app, parcel



class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.parcel = parcel
        self.new_parcel= {
            "userId": 3,
            "weight": 0.8,
            "pickup": "From",
            "destination": "To",
            "status": "pending"
            }
        self.status={
                        "status": "status"
                    }


    def tearDown(self):
        self.parcel.parcel_list=[]
    

    def test_parcel_type(self):
        self.assertIsInstance(self.parcel, ParcelList)


    def test_list_is_empty(self):
        self.assertFalse(ParcelList().get_all_parcels())


    def test_index(self):
        resp_get = self.client.get('/')
        self.assertEqual(resp_get.status_code, 200)


    def test_get_highest_parcel_id(self):
        self.assertEqual(self.parcel.get_highest_parcel_id(), 0)
        self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertEqual(self.parcel.get_highest_parcel_id(), 1)


    def test_add_parcel(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.assertEqual(len(self.parcel.get_all_parcels()), 0)
        resp_add = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertEqual(resp_add.status_code, 201)
        self.assertTrue(self.parcel.get_all_parcels())
        self.assertEqual(len(self.parcel.get_all_parcels()), 1)


    def test_get_parcel(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        resp_get = self.client.get('/api/v1/parcels/1')
        self.assertEqual(resp_get.status_code, 200)
        resp_get = self.client.get('/api/v1/parcels/4')
        self.assertEqual(resp_get.status_code, 400)


    def test_get_parcels_by_user(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        resp_get = self.client.get('/api/v1/users/3/parcels')
        self.assertEqual(resp_get.status_code, 200)
        resp_get = self.client.get('/api/v1/users/4/parcels')
        self.assertEqual(resp_get.status_code, 400)


    def test_get_all_parcel(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        resp_get = self.client.get('/api/v1/parcels')
        self.assertEqual(resp_get.status_code, 200)


    def test_cancel_order(self):
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('pending', str(resp_post.data))
        resp_chang = self.client.put('/api/v1/parcels/1/cancel', data=json.dumps(self.status), content_type='application/json')
        self.assertNotIn('pending', str(resp_chang.data))
        self.assertEqual(resp_chang.status_code, 200)
        resp_chang = self.client.put('/api/v1/parcels/4/cancel', data=json.dumps(self.status), content_type='application/json')
        self.assertEqual(resp_chang.status_code, 400)
    

    def test_weight_type(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.assertEqual(self.parcel.add_parcel(1, 1, '5.8', "j", "u", 'pending'), 'weight must be an Float!!')
    

    def test_no_weight(self):
        del self.new_parcel['weight']
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('Weight missing in data', str(resp_post.data))
    

    def test_no_userId(self):
        del self.new_parcel['userId']
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('User Id missing in data', str(resp_post.data))
    

    def test_no_status(self):
        del self.new_parcel['status']
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('Status missing in data', str(resp_post.data))
    

    def test_no_destination(self):
        del self.new_parcel['destination']
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('Destination missing in data', str(resp_post.data))
    

    def test_no_pickup(self):
        del self.new_parcel['pickup']
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('Pickup missing in data', str(resp_post.data))
    

    def test_data_type(self):
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps('string'), content_type='application/json')
        self.assertIn('Data must be in dictionary format', str(resp_post.data))
        self.assertEqual(resp_post.status_code, 400)


    def test_url_not_found(self):
        resp_get = self.client.get('/api/v1/parcels/parcel')
        self.assertEqual(resp_get.status_code, 404)



    def test_method_not_found(self):
        resp_get = self.client.put('/api/v1/parcels')
        self.assertEqual(resp_get.status_code, 405)
