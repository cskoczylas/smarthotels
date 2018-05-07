FROM ubuntu

# Update APT repos
RUN apt-get update --fix-missing

# Postgresql library
RUN apt-get install -y libpq-dev postgresql-client

# Python & Associated libraries
RUN apt-get install -y python3 python3-pip python3-dev
RUN pip3 install --upgrade pip

ADD requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

# Copy application files.
COPY index.py /src/index.py
COPY static/ManagementApp.html /src/static/ManagementApp.html
COPY postgresLibrary.py /src/postgresLibrary.py

# Add entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
# backwards compat
RUN ln -s usr/local/bin/docker-entrypoint.sh / 

ENTRYPOINT [ "docker-entrypoint.sh" ]