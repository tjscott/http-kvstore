#!/usr/bin/env python
import argparse
import sys

try:
    import plyvel
    from flask import abort, Flask, request
except ImportError:
    print "Modules 'Plyvel' and 'Flask' are required to run. Please ensure\
            they are installed (try pip install)."
    sys.exit(1)

# Set a default HTTP port
DEFAULT_HTTP_PORT = 4832

# Create the Flask app object
app = Flask(__name__)


# Application routing logic
@app.route('/')
def rootpath():
    return 'http-kvstore server'


@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    try:
        # Grab value from the DB
        value = db.get(str(key))
    except Exception, e:
        # Return internal server error if DB call fails
        abort(
                500, "Database error when accessing key '{}' ({})".format(
                    key, str(e)))

    # Return of 'None' indicates key doesn't exist, so test for a value
    if value:
        return value
    else:
        # Return a 404 if the key doesn't exist
        abort(404)


@app.route('/set/<key>', methods=['POST', 'PUT'])
def set_key(key):
    # Grab the contents of the 'message' field from user input
    try:
        print "Extracting value from request"
        value = request.form['message']
    except Exception, e:
        # Return internal server error if input can't be read
        print "Could not process input ({})".format(e)
        abort(500)
    if value:
        try:
            db.put(str(key), str(value))
            return('OK')
        except Exception, e:
            # Return internal server error if storing value fails
            print "Could not store message for key '{}' ({})".format(key, e)
            abort(500)
    else:
        # Return bad request if no value sent
        print "No value found for key '{}'".format(key)
        abort(400)


# Main loop to run Flask
if __name__ == '__main__':
    # HTTP listening port and a database directory are required to start.
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--port", "-p", type=int, default=DEFAULT_HTTP_PORT,
            help="specify port for HTTP server to listen on")
    parser.add_argument(
            "--db", "-d", type=str, nargs=1, required=True,
            help="location of LevelDB directory, will be created if non-existent")
    args = parser.parse_args()

    HTTP_PORT = args.port
    DB_DIR = args.db[0]  # Extract string from list

    print "Starting HTTP server on port {}, database located at {}...".format(
            HTTP_PORT, DB_DIR)

    # DB initialisation, creates the directory if non-existent
    try:
        db = plyvel.DB(DB_DIR, create_if_missing=True)
        print "Database started"
    except Exception, e:
        print "Error: Could not start database ({})".format(
                str(e))
    app.run(host="0.0.0.0", port=HTTP_PORT)
