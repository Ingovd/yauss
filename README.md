# Yet Another URL Shorting Service. #

This is my attempt at creating a scalable url shorting service.

## Setup ##

1. Clone repo and optionally set up a virtual environment using python's virtualenv
2. Run `pip install -r requirements.txt`
3. Edit `instance/config.py` to your liking
4. Run `python wsgi.py`

## Design ##

The system consists of three services.
1. yauss, which serves end users with a URL crud and URL redirects
2. a database, which stores all key-url pairs
3. a key store, which generates and serves guaranteed unique keys to yauss instances

If the system is run with the default configuration with no external database (MongoDB),
all three services are running on the same host.
The URL crud runs at http://server:port/, and the key store at http://server:port/keys/

To scale up the system, all services can be scaled individually (either horizontally or vertically).
The yauss service is designed so that many instances can run in parallel behind a reverse-proxy.
The database can be scaled by off-the-shelf solutions.
The key store can also be easily scaled, as it lends itself to trivial sharding (though this is not implemented).