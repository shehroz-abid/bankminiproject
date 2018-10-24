from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from MainUser import MainUser
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
api = Api(app)

user = MainUser()


def abort_user_isNotadmin(userid):
    if not user.isAdmin:
        abort(404, message="User is not admin".format(userid))

def abort_user_isNotavailable(username):
    if not user.username:
        abort(404, message="User is not available".format(username))


class User(Resource):
    #def get(self):

    def put(self, userid, amount):
        parser = reqparse.RequestParser()
        args = parser.parse_args()
        amount = {'amount': args['amount']}
        return amount, 201

    def delete(self, currentid, userid):
        abort_user_isNotadmin(currentid)
        abort_user_isNotavailable(userid)
        #del user.userid
        return '', 204


class SignInUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='username to Sign In')
            parser.add_argument('password', type=str, help='Password to Sign In')
            args = parser.parse_args()

            _userUsername = args['username']
            _userPassword = args['password']

            return {'Username': args['username'], 'Password': args['password']}

        except Exception as e:
            return {'error': str(e)}


class SignUpUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='username to Sign up user')
            parser.add_argument('password', type=str, help='Password to Sign up user')
            parser.add_argument('firstname', type=str, help='firstname to Sign up user')
            parser.add_argument('lastname', type=str, help='lastname to Sign up user')
            parser.add_argument('amount', type=str, help='amount to Sign up user')
            parser.add_argument('isAdmin', type=str, help='isAdmin to Sign up user')
            args = parser.parse_args()

            _userUsername = args['username']
            _userPassword = args['password']
            _userFirstname = args['firstname']
            _userLastname = args['lastname']
            _userAmount = args['amount']
            _userIsAdmin = args['isAdmin']

            return {'username': args['username'], 'password': args['password'], 'firstname': args['firstname'], 'lastname': args['lastname'], 'amount': args['amount'], 'isAdmin': args['isAdmin']}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(SignUpUser, '/SignUpUser')
api.add_resource(SignInUser, '/SignInUser')
api.add_resource(User, '/User/<user_id>')


if __name__ == '__main__':
    app.run(debug=True)

