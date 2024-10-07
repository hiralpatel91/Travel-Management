import logging
from flask_login import current_user
from flask import request,g
from Travel.User.routes import bp
from Travel import app

# set logging
# This line sets up logging for your Flask application,It allows you to track application 
# behavior and errors by logging messages to the console or a file, which is helpful for debugging
logging.basicConfig(level=logging.INFO)

# It logs the request method (GET, POST, etc.) and the path being requested. This information is 
# useful for monitoring and debugging
@bp.before_request
def before_request():
    logging.info(f"Request Method:{request.method},path: {request.path}")
    g.user = None
    if current_user.is_authenticated:
        g.user = current_user

# It adds security-related HTTP headers to the response
# X-Content-Type-Options: nosniff: Prevents browsers from MIME type sniffing, forcing them to stick to the declared content type.
# X-XSS-Protection: 1; mode=block: Enables cross-site scripting (XSS) filter in browsers, which helps mitigate XSS attacks.
# X-Frame-Options: DENY: Prevents your site from being framed, which can help protect against clickjacking attacks.
# These security headers help protect your application from common web vulnerabilities.

@bp.after_request
def add_headers(response):
    # security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

# Ensure that the JSON endpoint and other features are added as necessary
# This function checks if incoming POST or PUT requests to any endpoint that starts with /api have the correct Content-Type.
# This helps ensure that your API endpoints only accept JSON data, which can help maintain consistency and prevent errors
@app.before_request
def ensure_json_content():
    if request.method in ['POST', 'PUT'] and request.path.startswith('/api'):
        if not request.is_json:
            return {"error": "Content-Type must be application/json"}, 400


# This defines an API endpoint at /json-endpoint that accepts POST requests with JSON data
@app.route('/json-endpoint', methods=['POST'])
def json_endpoint():
    if request.is_json:  # Check if the request contains JSON data
        data = request.get_json()  # Parse the JSON data
        # Return a response with the received data
        return {"message": "Data received", "data": data}, 200
    else:
        return {"error": "Content-Type must be application/json"}, 400
