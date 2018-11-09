import json
from flask import *
from flask_restful import abort, Api, Resource, request
from flaskext.mysql import MySQL
from MainUser import MainUser


app = Flask(__name__, template_folder='.')
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BankDB'


mysql.init_app(app)
api = Api(app)

#mysql.init_app(app)


loginuser = MainUser()


"""def abort_user_isNotadmin(userid):
    if not user.isAdmin:
        abort(404, message="User is not admin".format(userid))

def abort_user_isNotavailable(username):
    if not user.username:
        abort(404, message="User is not available".format(username))
"""
#Update Method to update the Amount after Adding and Deducting

@app.route('/')
def main():
    try:
        if loginuser.get_username() == "":
            return render_template('index.html')
        else:
            return render_template('dashboard.html', data = loginuser.get_data(),
                                   amount=loginuser.get_amount(), password=loginuser.get_password())


    except Exception as e:
        return 'EXPOK'


@app.route('/SignOut', methods=['POST'])
def signout():
    try:
        loginuser.set_userid("")
        loginuser.set_username("")
        loginuser.set_password("")
        loginuser.set_firstname("")
        loginuser.set_lastname("")
        loginuser.set_amount("")
        loginuser.set_isadmin("")
        loginuser.set_data("")
        return render_template('index.html')

    except Exception as e:
        return 'EXPOK'


@app.route('/SignInUser', methods=['POST', 'GET'])
def sign_in_user():

    if request.method == 'POST':

        try:
            username = request.form['username']
            password = request.form['password']

            conn = mysql.connect()
            cursor = conn.cursor()

            sp_sign_in_user = "SELECT * FROM `User` WHERE `username`= %s"
            cursor.execute(sp_sign_in_user, username)

            #cursor.callproc('sp_SignInUser', (_userUsername,))

            data = cursor.fetchall()
            loginuser.set_data(data)
            data2 = json.dumps(data)

            if len(data) > 0:
                if data[0][2] == password:
                    loginuser.set_userid(data[0][0])
                    loginuser.set_username(data[0][1])
                    loginuser.set_password(data[0][2])
                    loginuser.set_firstname(data[0][3])
                    loginuser.set_lastname(data[0][4])
                    loginuser.set_amount(data[0][5])
                    loginuser.set_isadmin(data[0][6])

                    return render_template('dashboard.html', data = loginuser.get_data(),
                                           amount=loginuser.get_amount(), password=loginuser.get_password())
                    return {'Username': username, 'Password': password}
                else:
                    return 'InVLD PASS'
            else:
                return 'NotOK'
                return {'status': 100, 'message': 'Authentication failure'}

        except Exception as e:
            return 'EXPOK,'+username+"  " + data2 + loginuser.get_username()
            return {'error': str(e)}

    else:
        if loginuser.get_username() == "":
            return render_template('signin.html')
        else:
            return render_template('dashboard.html', data = loginuser.get_data(),
                                   amount = loginuser.get_amount(), password = loginuser.get_password())


@app.route('/GetDataAll', methods=['GET'])
def getalldata():

    try:

        conn = mysql.connect()
        cursor = conn.cursor()

        sp_get_all = "SELECT * FROM `User`"
        cursor.execute(sp_get_all)
        data = cursor.fetchall()
        data2 = json.dumps(data)

        return 'OK'+data2+" "

    except Exception as e:
        return 'EXPOK'


@app.route('/UpdatePassword',  methods=['POST', 'GET'])
def update_password():
    if request.method == 'POST':

        try:

            old_password = request.form['old_password']
            new_password = request.form['new_password']
            conn = mysql.connect()
            cursor = conn.cursor()

            if old_password == loginuser.get_password():

                sp_update_amount = "UPDATE `User` SET `password` = %s WHERE `User`.`username` = %s"
                cursor.execute(sp_update_amount, (new_password, loginuser.get_username()))
                conn.commit()

                loginuser.set_password(new_password)
                return render_template('dashboard.html', data=loginuser.get_data(),
                                       amount=loginuser.get_amount(), password=loginuser.get_password())
                return {'StatusCode': '200', 'Message': 'User Amount updated success'}
            else:
                return 'PSWRD INValid'

        except Exception as e:
            return 'EXPOK'+loginuser.get_username()
            return {'error': str(e)}

    else:
        return render_template('changepassword.html')


@app.route('/UpdateAmount',  methods=['POST', 'GET'])
def update_amount():
    if request.method == 'POST':
        try:
            amount = request.form['updated_amount']

            conn = mysql.connect()
            cursor = conn.cursor()

            '''user_amount = int.loginuser.get_amount()
    
            if amount > 0:
                new_amount = user_amount + amount
    
            elif amount < 0:
                new_amount = user_amount - amount
    
            else:
                return {"no change require"}'''

            sp_update_amount = "UPDATE `User` SET `amount` = %s WHERE `User`.`username` = %s"
            cursor.execute(sp_update_amount, (amount, loginuser.get_username()))
            conn.commit()
            #cursor.callproc('sp_updateAmount', (loginuser.get_username(), newamount,))

            loginuser.set_amount(amount)

            return render_template('dashboard.html', data = loginuser.get_data() ,
                                   amount= loginuser.get_amount(), password = loginuser.get_password())
            return {'StatusCode': '200', 'Message': 'User Amount updated success'}

        except Exception as e:
            return 'EXPOK'+amount+loginuser.get_username()
            return {'error': str(e)}
    else:
        return render_template('updateamount.html', amount = loginuser.get_amount())

#Delete Method to delete user


@app.route('/DeleteUser/<string:delt_username>',  methods=['DELETE'])
def delete_user(delt_username):

    try:

        conn = mysql.connect()
        cursor = conn.cursor()

        sp_check_admin = "SELECT `is_admin` FROM `User` WHERE `username` = %s"
        cursor.execute(sp_check_admin, loginuser.get_username())

        #cursor.callproc('sp_check_admin', (loginuser.get_username(),))
        data = cursor.fetchall()

        if data[0][0] == 0:

            return 'NOOK'
            #abort(404, message="User is not admin".format(loginuser.get_username()))
            #return {"You Are Not Admin"}

        elif data[0][0] == 1:
            sp_delete_user = "DELETE FROM `User` WHERE `User`.`username` = %s"
            cursor.execute(sp_delete_user, delt_username)
            conn.commit()

            return 'OKDone'
            #return {'StatusCode': '200', 'Message': 'User Deleted success'}

    except Exception as e:
        return 'EXPOK'
        #return {'error': str(e)}

#Post Method to sign In User /SignInUser?username=""&password=""


@app.route('/SignUpUser', methods=['POST', 'GET'])
def sign_up_user():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            amount = request.form['amount']
            is_admin = request.form['is_admin']
            conn = mysql.connect()
            cursor = conn.cursor()

            sp_check_exist = "SELECT * FROM User WHERE username = %(username)s"
            cursor.execute(sp_check_exist, {'username': username})

            data = cursor.fetchall()
            if len(data) is 0:
                sp_sign_up = "INSERT INTO `User` " \
                            "(`username`, `password`, `firstname`, `lastname`, `amount`, `is_admin`)" \
                            " VALUES (%s,%s,%s,%s,%s,%s);"

                cursor.execute(sp_sign_up, (username, password, firstname, lastname, amount, is_admin))
                conn.commit()
                return render_template('signin.html')
                return {'StatusCode': '200', 'Message': 'User creation success'}
            else:
                return 'ElSEOK'
                return {'StatusCode': '1000', 'Message': str(data[0])}

            return {'username': _userUsername, 'password': _userPassword, 'firstname': _userFirstName,
                    'lastname': _userLastName, 'amount': _userAmount, 'isAdmin': _userIsAdmin}

        except Exception as e:
            return 'EXPOKZ'+username+password+firstname+lastname+amount+is_admin
            return {'error': str(e)}
    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
