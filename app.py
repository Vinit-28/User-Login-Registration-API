# Importing the required modules #
from __init__ import *


# Instantiating the App #
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from SIRPI Products & Services Private Limited !!!"


# To login in the App #
@app.route('/login', methods=["GET"])
def login():

    userDetails = {
        "userName" : request.args["username"],
        "password" : request.args["password"],
    }
    result = {
        "requestStatus" : True,
    }

    if dbUtility.loginUser(userDetails = userDetails):
        result['loginSuccess'] = True
        result['responseMessage'] = "User Logged In Successfully !!!"
    else:
        result['loginSuccess'] = False
        result['responseMessage'] = "Invalid User Id or Password"

    return jsonify(result)


# User Registration #
@app.route('/register', methods = ["POST"])
def register():

    userDetails = {
        "userName" : request.args["username"],
        "password" : request.args["password"],
        "name" : request.args['name'],
        "description" : request.args['description'],
        "mobile" : request.args['mobile']
    }

    result = {
        "requestStatus" : True,
    }

    if dbUtility.registerUser(userDetails = userDetails):
        result['registrationSuccess'] = True
        result['responseMessage'] = "User Registered Successfully !!!"
    else :
        result['registrationSuccess'] = False
        result['responseMessage'] = "User Name Already Exists !!!"

    return jsonify(result)


# Getting all the registered users #
@app.route('/all_users', methods = ["GET"])
def all_users():

    result = {
        "requestStatus" : True,
        "requestFor" : "all_users",
        "registeredUsers" : dbUtility.getRegisteredAllUsers()
    }
    return jsonify(result)



# Logging out the user #
@app.route('/logout', methods = ["GET"])
def logout():

    result = {
        "requestStatus" : True,
    }

    if dbUtility.logoutUser(userName = request.args['username']):
        result['logoutSuccess'] = True
        result['responseMessage'] = "User Logged Out Successfully !!!"
    else:
        result['logoutSuccess'] = False
        result['responseMessage'] = "User Already Logged Out !!!"


    return jsonify(result)



# Reseting the User's Password #
@app.route('/reset_password', methods = ["PUT"])
def reset_password():

    userDetails = {
        "userName" : request.args['username'],
        "oldPassword" : request.args['old_password'],
        "newPassword" : request.args['new_password'],
    }

    result = {
        "requestStatus" : True
    }

    if dbUtility.resetUserPassword(userDetails = userDetails):
        result["passwordResetSuccess"] = True
        result["responseMessage"] = "User Password Reset Successfully !!!"
    else:
        result["passwordResetSuccess"] = False
        result["responseMessage"] = "Invalid User Id or Password !!!"

    return jsonify(result)



# Running the App #
if __name__ == "__main__":
    app.run(debug=True)