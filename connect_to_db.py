import sqlite3
from sql_startup import startup
from os.path import exists

def connect_to_db():
	try:
		cursor = None
		conn = None

		# only run startup script if the DB does not exist
		if not exists('./car_rental.db'):
			# Connect to DB
			conn = sqlite3.connect('car_rental.db')
			print("Connected to DB successfully")
			cursor = conn.cursor()

			cursor.executescript(startup)
			print("Ran startup DB script successfully")
		else:
			conn = sqlite3.connect('car_rental.db')
			print("Connected to DB successfully")
			cursor = conn.cursor()
			print("DB already exists so the startup script did not run")


		conn.close()

	except Exception as ep:
		print("Error connecting to DB", ep)
		conn.close()
	finally:
		conn.close()