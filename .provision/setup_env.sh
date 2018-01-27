#!/usr/bin/env bash

# reference: https://gist.github.com/davisford/8000332

echo "-------------------- updating package lists and installing packages"
apt-get update && apt-get install -y python-pip python-dev build-essential curl
apt-get install -y libpq-dev postgresql postgresql-contrib libmysqlclient-dev

# curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz
# tar xvfz virtualenv-1.10.1.tar.gz
# cd virtualenv-1.10.1
# sudo python setup.py install

# source "/vagrant/env/bin/activate"

pip install --index-url=https://pypi.python.org/simple/ -r /vagrant/requirements.txt

# fix permissions
echo "-------------------- fixing listen_addresses on postgresql.conf"
sed -i "s/#listen_address.*/listen_addresses '*'/" /etc/postgresql/9.1/main/postgresql.conf

echo "-------------------- fixing postgres pg_hba.conf file"
# replace the ipv4 host line with the above line
cat >> /etc/postgresql/9.1/main/pg_hba.conf <<EOF
# Accept all IPv4 connections - FOR DEVELOPMENT ONLY!!!
host    all         all         0.0.0.0/0             md5
EOF

echo "-------------------- creating postgres vagrant role with password vagrant"
# Create Role and login
sudo su postgres -c "psql -c \"CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD 'vagrant'\" "

echo "-------------------- creating wtm database"
# Create WTM database
sudo su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O vagrant wtm"

echo "-------------------- creating BucketlistApp database"
sudo su postgres -c "psql -c \"CREATE DATABASE BucketlistApp\" " 
sudo su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE BucketlistApp to vagrant\" "

echo "-------------------- creating vagrant database"
sudo su postgres -c "psql -c \"CREATE DATABASE vagrant\" " 
sudo su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE vagrant to vagrant\" "




### Define script variables
### ====================================================================================$

NAME="bucketlistapp application"                                        # Name of the application
DJANGODIR=/home/vagrant/bucketlistapp                                   # django project directo$
NUM_WORKERS=3                                                           # No. of worker processe$
DJANGO_SETTINGS_MODULE=bucketlistapp.settings                           # Settings file that Gun$
DJANGO_WSGI_MODULE=bucketlistapp.wsgi                                   # WSGI module name
DJANGO_PROD_DEBUG=True

### activate the virtualenv
### ====================================================================================$

echo "Starting $NAME as `whoami`"
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export DEBUG=$DJANGO_PROD_DEBUG
### Start Gunicorn
### ====================================================================================$

gunicorn bucketlistapp.wsgi --workers $NUM_WORKERS --bind 127.0.0.1:8000 --pythonpath=bucketlistapp
