from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask (__name__)
api = Api(app)

Userlist = {
    'username'
}

def abort_user_isNotadmin(userid):
    if not User.isAdmin:
        abort(404, message="User is not admin".format(userid))

def abort_user_isNotavailable(username):
    if not User.username:
        abort(404, message="User is not available".format(username))


parser = reqparse.RequestParser()
parser.add_argument('user')



class User(Resource):
    def get(self, userid):
