# http-kvstore
A simple HTTP server hosting a key-value store

Uses LevelDB via Plyvel as the backend, and Flask for HTTP serving and routing.

## Usage
Run `http-kvstore.py --port <port number> --db </path/to/leveldb/directory>`

The LevelDB directory will be created and initialised if it does not exist.

## Client API
### Get
Retrieve a stored `value` by querying against a `key` using HTTP GET:
```
curl -X GET http://kvstore-url:4832/get/<keyname>
```
Value is returned in a HTTP 200 response. 

### Set
Store a `value` for a given `key` using HTTP POST or PUT, with the value in the `message` field:
```
curl -X PUT http://kvstore-url:4832/set/<key> -d 'message=<value>'
```
OR
```
curl -X POST http://kvstore-url:4832/set/<key> -d 'message=<value>'
```
A successful set will return HTTP 200 with text `OK`.

HTTP 400 means the value was not found in the request, and a 500 indicates a different failure (possibly the database, see the return message for details).

## License
This is released under the MIT license.
