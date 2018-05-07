#!/usr/bin/python
import psycopg2
import psycopg2.extras
import csv

def main():
	conn = psycopg2.connect("host=localhost dbname=docker user=docker password=docker")
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cur.execute('SELECT * FROM guests')
	with open('us500.csv') as csvfile:
		reader = csv.reader(csvfile, delimiter=',',quotechar='|')
		next(reader) #skip the first(header) row
		for row in reader:
			first 	= row[0]
			last 	= row[1] 
			address = row[2]
			city 	= row[3]
			state 	= row[4]
			zipCode = row[5]
			phone 	= row[6]
			email 	= row[7]

			where	= "(first_name, last_name, address, city, state, zip, phone, email)"
			val 	= "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(first, last, address, city, state, zipCode, phone, email)
			insert_query = "INSERT INTO guests {} VALUES {}".format(where, val)
			cur.execute(insert_query)
			conn.commit()

	cur.close()
	conn.close()

if __name__ == '__main__':
	main()