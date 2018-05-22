### Entrance to the terminal Postgresql - psql

sudo -i -u postgres psql

### Create DB

CREATE DATABASE name_db;

### Create user from DB

CREATE USER name_user WITH password 'password';

### Granting user rights

GRANT ALL privileges ON DATABASE name_db TO name_user;
