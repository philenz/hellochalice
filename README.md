### Chalice Quickstart
* http://chalice.readthedocs.io/en/latest/quickstart.html
* https://aws.amazon.com/blogs/developer/category/python/

##### Hello World
* chalice new-project hellochalice
* chalice deploy
* http https://19bdrm9ink.execute-api.ap-southeast-2.amazonaws.com/api/

##### Hello Seattle
* http https://19bdrm9ink.execute-api.ap-southeast-2.amazonaws.com/api/cities/seattle

##### Error Handling
* BadRequestError - return a status code of 400
* UnauthorizedError - return a status code of 401
* ForbiddenError - return a status code of 403
* NotFoundError - return a status code of 404
* ConflictError - return a status code of 409
* TooManyRequestsError - return a status code of 429
* ChaliceViewError - return a status code of 500

##### Requests
The app.current_request object also has the following properties.
* current_request.query_params - A dict of the query params for the request.
* current_request.headers - A dict of the request headers.
* current_request.uri_params - A dict of the captured URI params.
* current_request.method - The HTTP method (as a string).
* current_request.json_body - The parsed JSON body (json.loads(raw_body))
* current_request.raw_body - The raw HTTP body as bytes.
* current_request.context - A dict of additional context information
* current_request.stage_vars - Configuration for the API Gateway stage

##### CORS
* You can specify whether a view supports CORS by adding the cors=True parameter to your @app.route() call.
* By default this value is false.
* If more fine grained control of the CORS headers is desired, set the cors parameter to an instance of CORSConfig instead of True.
* The CORSConfig object can be imported from the chalice package.

##### Libraries
* To add a code library use import chalicelib.xxxx
* Then create a directory called chalicelib containing xxxx.py and \_\_init\_\_.py

##### Authorization
* None
* chalice.IamAuthorizer()
* chalice.CognitoUserPoolAuthorizer()

##### Adding Standalone Lambda functions
* Use the @app.lambda_function decorator
* Example in sample chalice-trivia app to autoconfirm_user

##### Other Features
* @app.schedule for cron
* Dependency management
* AWS IAM policy generation
* Throttle API Gateway to defend against DDOS

##### Sample Code
* https://www.youtube.com/watch?v=0fMJqWLE6Iw
* https://github.com/philenz/chalice-trivia.git (cloned from youtube sample)