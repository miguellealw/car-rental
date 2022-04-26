import sqlite3
from sql_startup import startup
from os.path import exists

def connect_to_db(db_name):
	try:
		conn = None

		# only run startup script if the DB does not exist
		if not exists('./' + db_name):
			# Connect to DB
			conn = sqlite3.connect(db_name)
			print("Connected to DB successfully")
			cursor = conn.cursor()

			cursor.executescript(startup)
			print("Ran startup DB script successfully")
		else:
			conn = sqlite3.connect(db_name)
			print("Connected to DB successfully")
			cursor = conn.cursor()
			print("DB already exists so the startup script did not run")

	except Exception as ep:
		print("Error connecting to DB", ep)
	
	return conn