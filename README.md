# Smart Hotels
UConn CSE 2018 SDP Team 16 : Smart Hotels

## Prerequisites
- You will need both `docker` and `docker-compose` installed.

## Usage
```bash
# In the project directory...

# Build The image
docker-compose build

# Bring the container up
docker-compose up

# You can also start them in the background:
docker-compose start
```

## Production usage
```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml create
docker-compose -f docker-compose.prod.yml start
```

## Connecting to the docker container
```bash
psql -U docker -d docker -h localhost -p 5432
```

## To see the database or a specific one, or working with the tables
`\?` will list all the commands

`\q` will quit

`\d` will list tables

`\d <tablename>` will show the columns and data types in a table

`SELECT * FROM <tablename>;` will show the actual table, pretty much the basic sql statement

`psql -U docker -d docker -h localhost -p 5432 -f postgres\drop_schema.sql` to drop tables and start from scratch

`psql -U docker -d docker -h localhost -p 5432 -f postgres\create_schema.sql` to create all the tables

`psql -U docker -d docker -h localhost -p 5432 -f postgres\insertTestData.sql` to add the test data

password is `docker`

## Contributors :
- Rafal Bzeubik
- Arun George
- Rich Infante
- Brian Matuszak 
- Kevin Schumitz
- Christopher Skoczylas
