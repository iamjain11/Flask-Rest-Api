from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

app.config['SECRET_KEY'] = './private_key.pem'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is required'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route("/")
@app.route("/home")
def hello():
    return "Home Page!"


@app.route('/contact')
def contact():
    return jsonify({'about': 'hello world!'}), 201


@app.route('/user', methods=['GET', 'POST'])
@token_required
def user():
    if request.method == 'POST':
        user_data = request.get_json()
        return jsonify({'user': user_data})
    else:
        return jsonify({'user': [
            {
                'name': 'manoj'
            },
            {
                'name': 'dinesh'
            }
        ]}), 201


@app.route('/multi/<int:num>', methods=['GET'])
def get_mulitply_10(num):
    return jsonify({'result': num*10}), 201


@app.route("/about")
def about():
    return "about page!"


@app.route("/login")
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode(
            {
                'user': auth.username,
                'exp': exp
            },
            app.config['SECRET_KEY']
        )
        return jsonify({
            'token': token,
            'exp': exp,
            'username': auth.username
        })

    return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})


if __name__ == "__main__":
    app.run(debug=True)
# FLASK_APP=my-app.py FLASK_DEBUG=1 flask run
