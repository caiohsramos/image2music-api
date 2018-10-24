from flask import Flask
import os
from flask_cors import CORS
from functools import wraps
from flask import request, Response

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

@app.route('/api/watson')
#@requires_auth
def watson():
    return 'OK'
@app.route('/api/spotify')
#@requires_auth
def spotify():
    return 'OK'



if __name__=='__main__':
    app.run(host='0.0.0.0',port=3001)