from typing import Final, Union
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
POSTGRES_DBNAME: Final[Union[str, None]] = os.getenv("POSTGRES_DBNAME")
POSTGRES_USER: Final[Union[str, None]] = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD: Final[Union[str, None]] = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST: Final[Union[str, None]] = os.getenv("POSTGRES_HOST")
POSTGRES_PORT: Final[Union[str, None]] = os.getenv("POSTGRES_PORT")

connection = psycopg.connect(
		dbname=POSTGRES_DBNAME,
		user=POSTGRES_USER,
		password=POSTGRES_PASSWORD,
		host=POSTGRES_HOST,
		port=POSTGRES_PORT)
cursor = connection.cursor()

"""
cursor.execute("CREATE TABLE IF NOT EXISTS counter (channel integer PRIMARY KEY, count integer, last_responder integer, record integer);")
cursor.execute("INSERT INTO counter (channel, count, last_responder, record) VALUES (2, 2, 2, 2)")
connection.commit()
cursor.execute("SELECT * FROM counter;")
dataset = cursor.fetchall()
test = {}
for item in dataset:
	test[item[0]] = item[1:]
print(test)
"""

"""
cursor.execute("SELECT * FROM test")
dataset = cursor.fetchall()

for data in dataset:
	print(data)

cursor.close()
connection.close()
"""
