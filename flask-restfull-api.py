from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        user_data = request.get_json()
        return jsonify({'user': user_data})


class User(Resource):
    def get(self):
        return {
            'users': [
                {
                    'name': 'mohan'
                },
                {
                    'name': 'ravi'
                }
            ]
        }

    def post(self):
        user_data = request.get_json()
        return jsonify({'user': user_data})


class Multi(Resource):
    def get(self, num):
        return {'result': num*10}


api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user')
api.add_resource(Multi, '/multi/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
