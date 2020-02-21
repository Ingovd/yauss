# Yet Another URL Shorting Service. #

This is my attempt at creating a URL shorting service with scalability in mind.


## Setup ##

1. Clone repo and optionally set up a virtual environment using python's virtualenv
2. Run `pip install -r requirements.txt`
3. Edit `instance/config.py` to your liking
4. Run `python wsgi.py`


## Client-side Usage ##

When the system is running, the two main responsibilities of the service
is to receive new URL entries and redirect existing keys to their corresponding URL.

If the service is running at `http://hostname/`, this address provides a basic CRUD
for adding URLs. For testing purposes, it also offers update/delete functionality
(though these don't work well with caching).
Once a URL has been added, the user is given the shortened URL of the form `http://hostname/<key>`.
Visiting this address with a valid key will result in a http redirect to the corresponding URL.

## Server-side Design Overview ##

The system consists of three services.
1. yauss, the service exposed to clients which accepts URLs and redirects
2. a key store, which generates and serves guaranteed unique keys to yauss instances
3. a database, which stores all key-URL pairs

If the system is run with the default configuration with no external database (MongoDB),
all three services are running on the same host,
with the key store api available at `http://hostname/keys/`


### Yauss ###

In order to serve clients, this service needs to map keys to URLs and
be able to add new entries to the map.
Internally, this map is accessible to the server through a simple MutableMapping interface,
which is backed by an external MongoDB.
Adding new entries to the map requires unique keys, and in order to unburden the database backing the map
from authorising new keys, this responsibility is deferred to the *key store*.
The key store is available to yauss through a simple RESTful API:
a GET to `http://keystore/request/<n>;` provides (up to) n guaranteed unique keys,
and a GET to `http://keystore/approve/<key>` returns True if the key is available
(any future approval attempts of the same key will returns False)

The main non-functional requirement (besides correctness) for this service is to respond quickly;
most importantly, redirects should be snappy.
In order to facilitate this, yauss supports simple caching of redirects (backed by a python map),
or (an untested) redis cache.
Furthermore, new entries into the map should also happen quickly, and in order
to facilitate this, yauss maintains a cache of unique keys to employ.

*Note*: in the current implementation, this cache is backed by python's set container (which is not thread safe).
A better solution for the cache would be a thread safe circular buffer, so that a worker thread can periodically
refill the cache without blocking the consuming end of the buffer.

### Key Store ###

Each key is a 48-bit value, encoded as 8 digit base-64 number.
The currrent implementation of the key store uses an sqlite or MongoDB database to store all keys that
have been requested or approved by a yauss service.
The generation of keys is currently handled by simply sampling the key space randomly and verifying whether
it exists in the underlying database.
*Note*: to expedite the prototype implementation,
keys are currently transmitted encoded in a json text format,
though sending plain bytes is preferred in an actualy system.

### Database ###

The database is the authority over the key-URL map.


## Scaling Up ##

To scale up the system, all services can be scaled individually (either horizontally or vertically).
The yauss service is designed so that many instances can run in parallel behind a reverse-proxy.
