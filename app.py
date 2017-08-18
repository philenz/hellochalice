import sys
import os
import json
import boto3
import logging

from botocore.exceptions import ClientError
from chalice import Chalice, BadRequestError, NotFoundError, Response

if sys.version_info[0] == 3:
    from urllib.parse import urlparse, parse_qs
else:
    from urlparse import urlparse, parse_qs

app = Chalice(app_name='hellochalice')
app.debug = True
app.log.setLevel(logging.DEBUG)

app.log.debug("Debugging hellochalice!")

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

S3 = boto3.client('s3', region_name='ap-southeast-2')
BUCKET = 'hellochalice'



@app.route('/', cors=True)
def index():
    return {
        'hello': os.environ['DB_TABLE']
    }

# use different content type than default application/json
# http --form POST https://19bdrm9ink.execute-api.ap-southeast-2.amazonaws.com/api/ states=CA states=CA --debug
# use httpie's --form to set content type
#
# if not using application/json, use raw_body instead of the usual json_body
@app.route('/raw', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def rawindex():
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
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT':
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)

# dump request
# http 'https://endpoint/api/introspect?query1=value1&query2=value2' 'X-TestHeader: Foo'
@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

# define our response
@app.route('/hello')
def respindex():
    return Response(body='hello world!',
                    status_code=200,
                    headers={'Content-Type': 'text/plain'})
