import sys

from chalice import Chalice, BadRequestError, NotFoundError

if sys.version_info[0] == 3:
    from urllib.parse import urlparse, parse_qs
else:
    from urlparse import urlparse, parse_qs

app = Chalice(app_name='hellochalice')
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

OBJECTS = {
}

# use different content type than default application/json
# http --form POST https://19bdrm9ink.execute-api.ap-southeast-2.amazonaws.com/api/ states=CA states=CA --debug
# use httpie's --form to set content type
@app.route('/', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def index():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {
        'states': parsed.get('states', [])
    }

@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))

@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}


@app.route('/users', methods=['POST'])
def create_user():
    # This is the JSON body the user sent in their POST request.
    user_as_json = app.current_request.json_body

    # We'll echo the json body back to the user in a 'user' key.
    return {'user': user_as_json}

# PUT something with...
# echo '{"foo":"bar"}' | http PUT https://19bdrm9ink.execute-api.ap-southeast-2.amazonaws.com/api/objects/mykey
# GET it...
# http https://19bdrm9ink.execute-api.ap-southeast-2.amazonaws.com/api/objects/mykey
@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)

# dump request
# http 'https://endpoint/api/introspect?query1=value1&query2=value2' 'X-TestHeader: Foo'
@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()



