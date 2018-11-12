import json
import unittest
from app.model import ParcelList

from app.views import app, parcel



class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        # self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.parcel = parcel
        self.new_parcel={
                            "weight": 5.9,
                            "status": "pending",
                            "destination": "to",
                            "pickup": "from"
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


    def test_get_all_parcel(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        resp_get = self.client.get('/api/v1/parcels')
        self.assertEqual(resp_get.status_code, 200)


    def test_change_status(self):
        self.assertFalse(self.parcel.get_all_parcels())
        resp_post = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json')
        self.assertIn('pending', str(resp_post.data))
        resp_chang = self.client.put('/api/v1/parcels/1', data=json.dumps(self.status), content_type='application/json')
        self.assertNotIn('pending', str(resp_chang.data))
        self.assertEqual(resp_chang.status_code, 200)
        resp_chang = self.client.put('/api/v1/parcels/4', data=json.dumps(self.status), content_type='application/json')
        self.assertEqual(resp_chang.status_code, 400)
    

    def test_weight_type(self):
        self.assertFalse(self.parcel.get_all_parcels())
        self.assertEqual(self.parcel.add_parcel(1, '5', 'pending', "j", "u"), 'weight must be an Float!!')


    def test_url_not_found(self):
        resp_get = self.client.get('/api/v1/parcels/parcel')
        self.assertEqual(resp_get.status_code, 404)
