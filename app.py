from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import time

app = Flask(__name__)
SERVER_SECRET_KEY = "5973598a5b9cba6ebb36d2f95019442d2f1994e378a5928da10f235fecc10ac0"
CORS(app)
database = { }


# =====================================================================
# Funtion sitess here, Create Funtion Here
# =====================================================================
def check_email(email):
    for id , info in database.items():
        if info["email"] == email:
            return False
    return True        


def check_password(p1 , p2):
    if p1 == p2:
        return True
    return False


#creating token for logining
def Create_token(id , name):
    payload = {
        "id" : id ,
        "name" : name ,
        "exp" : time.time() + 1000
     }
    token = jwt.encode(payload , SERVER_SECRET_KEY.encode() , algorithm='HS256')
    return token



def check_login(l_email, l_password):
    for id , info in database.items():
        if info['email'] == l_email and info['password'] == l_password:
            return True , id , info['name']
            break 
    return False

# =====================================================================
# ROUTE 1: Register (Happens ONCE - Generates the Token + Extra Info)
# =====================================================================

@app.route('/api/register', methods=['POST' , 'GET'])
def register():
    if request.method == "POST":
        data = request.get_json()
        is_found = check_email(data["email"])
        if not is_found:
            return jsonify({"status": "Error", "message": "Email Already Exists" }), 401
        else:
            is_pass = check_password(data["password"] , data["C_password"])
            if not is_pass:
                return jsonify({"status": "Error", "message": "Password Already Exists" }), 401
            else:
                id = len(database) + 1
                database[id] = {
                    "name" : data["name"] ,
                    "email" : data["email"] ,
                    "password" : data["password"],
                    "C_password": data["C_password"]
                }
                token = Create_token(id , data["name"])

                return jsonify({"status": "success", 'token': token }), 200



# =====================================================================
# ROUTE 1: Login (Usually happens - Generates the Token + Extra Info)
# =====================================================================

@app.route("/api/login" , methods =["Post"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data['email']
        password = data['password']
        is_found  , id , name= check_login(email , password)
        if not is_found:
            return jsonify({"status":"error" , "message": "Either email or password is incorrect"}) , 401
        else:
    
            token = Create_token(id , name)
            return jsonify({"status": "success", 'token': token }), 200


 


# =====================================================================
# ROUTE 1: Login (Usually happens - Generates the Token + Extra Info)
# =====================================================================

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"status": "error", "message": "Token is missing!"}), 401

    try:
        data = jwt.decode(token, SERVER_SECRET_KEY.encode(), algorithms=['HS256'])
        id = data['id']
        return jsonify({
            "status": "success",
            "secret_data": f"Welcome {database[id]['name']}! Here is your highly secure data."
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired", "message": "Your session has expired. Please login again."}), 401
        
    except jwt.InvalidTokenError:
        return jsonify({"status": "error", "message": "Invalid token!"}), 401






if __name__ == '__main__':
    app.run(debug=True)


        





