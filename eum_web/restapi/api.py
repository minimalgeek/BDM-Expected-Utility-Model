'''
Created on 2016 jún. 14

@author: Balázs
'''

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            return {'Email': args['email'], 'Password': args['password']}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/CreateUser')

if __name__ == '__main__':
    app.run(debug=True)