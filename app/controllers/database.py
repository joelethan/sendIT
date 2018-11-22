from flask import jsonify
import psycopg2
import os

class DatabaseConnection:
	def __init__(self):
		try:
			postgres = "sendit"
			if os.getenv('APP_SETTINGS') == 'testing':
				postgres = "test_db"
			self.connection = psycopg2.connect(database=postgres,
								user="postgres",
								host="localhost",
								password="postgres",
								port="5432")
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()

		except Exception as e:
			print(e)
			print('Failed to connect to db')


	def create_tables(self):

		""" Create all database tables"""

		create_table = "CREATE TABLE IF NOT EXISTS users \
			( user_id SERIAL PRIMARY KEY, username VARCHAR(20), \
			email VARCHAR(100), password VARCHAR(100), admin BOOLEAN NOT NULL);"
		self.cursor.execute(create_table)

		create_table = "CREATE TABLE IF NOT EXISTS parcel_orders \
			( parcel_id SERIAL PRIMARY KEY, weight FLOAT,\
			user_id INTEGER NOT NULL REFERENCES users(user_id), \
			pickup_location VARCHAR(20), destination VARCHAR(20), \
			present_location VARCHAR(20), status VARCHAR(20));"
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


	def place_order(self, user_id, weight, pickup_location, present_location, destination):
		query = "INSERT INTO parcel_orders (user_id, weight, pickup_location, \
			present_location, destination, status)\
			VALUES ('{}', '{}', '{}','{}', '{}', 'New');\
			".format(user_id, weight, pickup_location, present_location, destination)
		self.cursor.execute(query)


	def drop_tables(self):
		query = "DROP TABLE parcel_orders;DROP TABLE users; "
		self.cursor.execute(query)
		return "Droped"


	def get_orders(self):
		query = "SELECT * FROM parcel_orders;"
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
		user = self.cursor.fetchone()
		return user

	def validate_data(self, value, lst):
		if value not in lst:
			return jsonify({'message':'{} field must be present'.format(value)}), 400