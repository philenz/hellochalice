from chalice import Chalice, BadRequestError

app = Chalice(app_name='hellochalice')
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}


@app.route('/')
def index():
    return {'hello': 'world'}

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
