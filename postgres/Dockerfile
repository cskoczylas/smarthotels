FROM library/postgres

# Copy Schema to docker container and create tables
COPY create_schema.sql /docker-entrypoint-initdb.d/10-schema.sql 

