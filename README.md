# Yet Another URL Shorting Service. #

This is my attempt at creating a URL shorting service with scalability in mind.
The web application is written in **python 3.8** using the Flask web framework.
I chose Flask both because of it's microarchitecture nature, making it a good fit for this project,
and because I wanted to learn something new (I had some experience using PHP and Django).

A live version of the system is running at http://yauss.tk.


## Setup ##

1. Clone repo and optionally set up a virtual environment using python's virtualenv
2. Run `pip install -r requirements.txt`
3. Edit `instance/config.py` to your liking
4. Run `python wsgi.py`


## Client-side Usage ##

When the system is running, the two main responsibilities of the service
is to receive new URL entries and redirect existing keys to their corresponding URL.

If the service is running at `http://hostname/`, this address provides a basic CRUD
for adding URLs.
The update/delete functionality is mostly there fore testing,
and these don't work well with caching.
Once a URL has been added, the user is given the shortened URL of the form `http://hostname/<key>`.
Visiting this address with a valid key will result in a http redirect to the corresponding URL.

## Server-side Design Overview ##

The system consists of three services.
1. yauss, the service exposed to clients which accepts URLs and redirects
2. a key store, which generates and serves guaranteed unique keys to yauss instances
3. a database, which stores all key-URL pairs

If the system is run with the default configuration with no external database (MongoDB),
all three services are running on the same host, with the key store api available at `http://hostname/keys/`.
The live system has its key store running on a different host, at the address http://keys.yauss.tk


### Yauss ###

In order to serve clients, this service needs to map keys to URLs and
be able to add new entries to the map.
Internally, this map is accessible to the server through a simple MutableMapping interface,
which is backed by an external MongoDB.
Adding new entries to the map requires unique keys, and in order to unburden the database backing the map
from authorising new keys, this responsibility is deferred to the *key store*.
The key store is available to yauss through a simple RESTful API:
a GET to `http://keystore/request/<n>` provides (up to) n guaranteed unique keys.

The main non-functional requirement (besides correctness) for this service is to respond quickly;
most importantly, redirects should be snappy.
In order to facilitate this, yauss supports simple caching of redirects (backed by a python map),
or (an untested) redis cache.
Furthermore, new entries into the map should also happen quickly, and in order
to facilitate this, yauss maintains a pool of unique keys to employ (cached from the key store).

**Note**: in the current implementation, this pool is backed by python's set container (which is not thread safe).
A better solution for the pool would be a thread safe circular buffer, so that a worker thread can periodically
refill the pool without blocking the consuming end of the buffer.

### Key Store ###

Each key is a 48-bit value, encoded as 8 digit base-64 number.
The currrent implementation of the key store uses an sqlite or MongoDB database to store all keys that
have been requested or approved by a yauss service.
The generation of keys is currently handled by simply sampling of the key space randomly and verifying whether
it exists in the underlying database.

Besides a GET to `/request/<n>`, the key store api also supports
a GET to `http://keystore/approve/<key>`, which returns True if the key is available
(any future approval attempts of the same key will returns False).
This functionality is currently not used, but was included in the api to
support custom keys in the future.

**Note 1**: to expedite the prototype implementation,
keys are currently generated and transmitted text format,
though representing them as plain bytes is preferred in an actual system.

**Note 2**: Currently, once a key has been generated it can never be used again.
In order for the system to be a bit more durable w.r.t. to the key pool (though 2^48 is quite substantial),
keys can be given an expiration time.
It is then up to yauss to insert key-URL pairs so that the URL expiration is less than the key expiration.
Finally, when a key is generated whose expiration time has passed, the key can be used again.
To still faciliate simple caching of keys at the yauss service, it can maintain multiple key caches with
e.g. 1 week, 1 month, 1 year, and indefinite expiration times.

### Database ###

The database is the authority over the key-URL map.


## Scaling Up ##

To scale up the system, all services can be scaled individually (either horizontally or vertically).
The yauss service is designed so that many instances can run in parallel behind a reverse-proxy,
since it only depends on a mutable mapping api and the key store api.
Both of these can be scaled horizontally by a simple key-prefix-sharding strategy.

**Note**: Since the current system has no (intended) way of removing key-URL pairs from the system,
cache invalidation is not an issue.
However, if users are allowed to delete their keys (eitherr manually or through expiration),
then scalable cache invalidation strategies need to be taken into account.
The expiration of key-URL pairs can easily be handled with any caching strategy by simply adding
the expiration date to the cache; when an expired URL is requested, it is simply removed from
whatever cache it was in.
To support manual deletion (or even updates) of URLs, we could let key-URL pairs be cached
for only a limited amount of time, meaning that a delete/update would only be visible after
the cache has expired.
