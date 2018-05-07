import psycopg2
import csv

conn = psycopg2.connect("dbname=docker user=docker password=docker host=postgres")
cur = conn.cursor()
with open('us-500.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',',quotechar='|')
	next(reader) #skip the first(header) row
	for row in reader:
		# first, last, address, city, state, zip, phone, email = 
		# row['first_name'],row['last_name'],row['address'],row['city'],row['state'],row['zip'],row['phone1'],row['email']
		first = row['first_name']
		last = row['last_name'] 
		address = row['address']
		city = row['city']
		state row['state']
		zipCode = row['zip']
		phone = row['phone1']
		email = row['email']

		str = "('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(first, last, address, city, state, zipCode, phone, email)
	
		insert_query = "INSERT INTO guests VALUES {}".format(str);
		cur.execute(insert_query)
		conn.commit()