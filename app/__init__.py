

import os
import jwt
from functools import wraps
from flask import Flask, _app_ctx_stack
from flask_cors import cross_origin
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from werkzeug.security import safe_str_cmp

# Custom JSON returns
class JSON_API_Message:
    JSON_200_OK = {"200":"OK"}
    JSON_204_NO_CONTENT = {"204": "NO CONTENT"}



app = Flask(__name__)

# Format error response and append status code.
def handle_error(error, status_code):
    resp = jsonify(error)
    resp.status_code = status_code
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client_id = '9NfstblRp1Rcp9v9tJiQhS4CyzXN3eJT'
        client_secret ='jUwAL_nTmeZXtflz6SaIj905_9VHzkKMMEThtLYdh5i7voDmR7f66mL_RGZYRN82'
        auth = request.headers.get('Authorization', None)
        if not auth:
            return handle_error({'code': 'authorization_header_missing',
                                'description':
                                    'Authorization header is expected'}, 401)

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return handle_error({'code': 'invalid_header',
                                'description':
                                    'Authorization header must start with'
                                    'Bearer'}, 401)
        elif len(parts) == 1:
            return handle_error({'code': 'invalid_header',
                                'description': 'Token not found'}, 401)
        elif len(parts) > 2:
            return handle_error({'code': 'invalid_header',
                                'description': 'Authorization header must be'
                                 'Bearer + \s + token'}, 401)

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                client_secret,
                audience=client_id
            )
        except jwt.ExpiredSignature:
            return handle_error({'code': 'token_expired',
                                'description': 'token is expired'}, 401)
        except jwt.InvalidAudienceError:
            return handle_error({'code': 'invalid_audience',
                                'description': 'incorrect audience, expected: '
                                 + client_id}, 401)
        except jwt.DecodeError:
            return handle_error({'code': 'token_invalid_signature',
                                'description':
                                    'token signature is invalid'}, 401)
        except Exception:
            return handle_error({'code': 'invalid_header',
                                'description': 'Unable to parse authentication'
                                 ' token.'}, 400)

        _app_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)

    return decorated

# No auth required
@app.route('/ping')
@cross_origin(headers=['Content-Type', 'Authorization'])
def ping():
    return "Good to go"

# Auth required
@app.route('/secured/ping')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def securedPing():
    return "Good to go, you're authenticated"




# Setup static path for Flask to render from
static_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'), 'static')

app._static_folder = static_path

# Configuration
app.config.from_object('config')


# Define database object
db = SQLAlchemy(app)

from app.mod_organization.controllers import bp_app as bp_app_module
from app.mod_organization.controllers import bp_organization as bp_organization_module
app.register_blueprint(bp_app_module)
app.register_blueprint(bp_organization_module)
db.create_all()
