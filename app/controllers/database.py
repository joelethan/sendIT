from flask import jsonify
import psycopg2
import os

class DatabaseConnection:
	def __init__(self):
		try:
			postgres = "ddqts6ki9k1l1r"
			if os.getenv('APP_SETTINGS') == 'testing':
				postgres = "test_db"
			self.connection = psycopg2.connect(database=postgres,
								user="wkwcyfqrkphlfc",
								host="ec2-174-129-41-12.compute-1.amazonaws.com",
								password="44a313d7ef9109d23ea6bf37034166ca9491a96179f8d6b794337224e22b7539",
								port="5432")
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()

		except Exception as e:
			print(e)
			print('Failed to connect to db')


	def create_tables(self):

		""" Create all database tables"""

		create_table = "CREATE TABLE IF NOT EXISTS users \
			( user_id SERIAL PRIMARY KEY, username VARCHAR(20) UNIQUE, \
			email VARCHAR(100), password VARCHAR(100), admin BOOLEAN NOT NULL);"
		self.cursor.execute(create_table)

		create_table = "CREATE TABLE IF NOT EXISTS parcel_orders \
			( parcel_id SERIAL PRIMARY KEY, weight FLOAT,\
			user_id INTEGER NOT NULL REFERENCES users(user_id), \
			username VARCHAR(20) NOT NULL REFERENCES users(username), \
			pickup_location VARCHAR(20), destination VARCHAR(20), \
			present_location VARCHAR(20), status VARCHAR(20), date DATE NOT NULL DEFAULT LOCALTIMESTAMP(0));"
		self.cursor.execute(create_table)


	def add_user(self, username, email, password):
		query = "INSERT INTO users (username, email, password, admin) VALUES\
			('{}', '{}', '{}', False);".format(username, email, password)
		self.cursor.execute(query)


	def get_user(self, column, value):
		query = "SELECT * FROM users WHERE {} = '{}';".format(column, value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		return user


	def promote_user(self, order_id):
		query = "UPDATE users SET admin = True WHERE user_id = '{}';\
		".format(order_id)
		self.cursor.execute(query)


	def auto_admin(self):
		query = "UPDATE users SET admin = True WHERE user_id < 2;"
		self.cursor.execute(query)


	def place_order(self, user_id, username, weight, pickup_location, present_location, destination):
		query = "INSERT INTO parcel_orders (user_id, username, weight, pickup_location, \
			present_location, destination, status)\
			VALUES ('{}', '{}', '{}', '{}','{}', '{}', 'New');\
			".format(user_id, username, weight, pickup_location, present_location, destination)
		self.cursor.execute(query)


	def drop_tables(self):
		query = "DROP TABLE parcel_orders;DROP TABLE users; "
		self.cursor.execute(query)
		return "Droped"


	def get_orders(self):
		query = "SELECT * FROM parcel_orders ORDER BY parcel_id ASC;"
		self.cursor.execute(query)
		orders = self.cursor.fetchall()
		return orders


	def get_user_orders(self, id):
		query = "SELECT * FROM parcel_orders where user_id = {};".format(id)
		self.cursor.execute(query)
		orders = self.cursor.fetchall()
		return orders


	def get_user_id(self, id):
		query = "SELECT user_id FROM parcel_orders WHERE parcel_id = '{}';".format(id)
		self.cursor.execute(query)
		user_id = self.cursor.fetchone()[0]
		return user_id


	def update_destination(self, order_id, destination):
		query = "UPDATE parcel_orders SET destination = '{}' WHERE parcel_id = '{}';\
		".format(destination, order_id)
		self.cursor.execute(query)


	def update_status(self, order_id, status):
		query = "UPDATE parcel_orders SET status = '{}' WHERE parcel_id = '{}';\
		".format(status, order_id)
		self.cursor.execute(query)


	def update_presentLocation(self, order_id, location):
		query = "UPDATE parcel_orders SET present_location = '{}' WHERE parcel_id = '{}';\
		".format(location, order_id)
		self.cursor.execute(query)


	def get_an_order(self, column, value):
		query = "SELECT * FROM parcel_orders WHERE {} = '{}'".format(column, value)
		self.cursor.execute(query)
		parcel = self.cursor.fetchone()
		return parcel


	def validate_data(self, value, lst):
		if value not in lst:
			return jsonify({'message':'{} field must be present'.format(value)}), 400 


	def get_item_from_parcels(self, item, value):
		query = "SELECT {} FROM parcel_orders WHERE parcel_id = '{}'".format(item, value)
		self.cursor.execute(query)
		item = self.cursor.fetchone()
		return item 

	def get_created_parcel(self):
		query = "SELECT * from parcel_orders ORDER BY parcel_id DESC LIMIT 1"
		self.cursor.execute(query)
		item = self.cursor.fetchone()
		return item 
