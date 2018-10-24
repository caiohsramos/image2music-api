from flask import Flask
import os
from flask_cors import CORS
from functools import wraps
from flask import request, Response, jsonify
import requests

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == os.environ['USERNAME'] and password == os.environ['PASSWORD']

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)
CORS(app)

@app.route('/api/watson', methods=['POST','OPTIONS'])
@requires_auth
def watson():
    endpoint_api = 'https://gateway.watsonplatform.net/visual-recognition/api/v3/classify'
    endpoint_token = 'https://iam.bluemix.net/identity/token'

    headers_token = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    request_data = {
        'grant_type': "urn:ibm:params:oauth:grant-type:apikey",
        'apikey': os.environ['API'],
    }

    params_api = {
        'version': '2018-03-19',
        'url': request.get_json()['url'],
    }

    r = requests.post(endpoint_token, data=request_data, headers=headers_token)

    r_final = requests.get(endpoint_api, headers = {
                    'Authorization': 'Bearer ' + r.json()['access_token'],
                    'Accept-Language': 'en',
                },
                params = params_api)
    return jsonify(r_final.json())
    
@app.route('/api/spotify', methods=['POST','OPTIONS'])
@requires_auth
def spotify():
    endpoint_token = 'https://accounts.spotify.com/api/token'
    endpoint_api = 'https://api.spotify.com/v1/search'
    headers_token = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body_token = {
        'grant_type': 'client_credentials',
    }
    auth = (os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])

    r = requests.post(endpoint_token, data=body_token, auth=auth, headers=headers_token)
    r_final = requests.get(endpoint_api, 
        headers={ 'Authorization': 'Bearer ' + r.json()['access_token'] },
        params= { 'q': request.get_json()['query'], 'type': 'track' })
    return jsonify(r_final.json())




if __name__=='__main__':
    app.run(host='0.0.0.0',port=os.environ['PORT'])