from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import jwt
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = "5973598a5b9cba6ebb36d2f95019442d2f1994e378a5928da10f235fecc10ac0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


# =====================================================================
# Funtion sitess here, Create Funtion Here
# =====================================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),  nullable=False)
    email = db.Column(db.String(50) , nullable=False , unique=True)
    password = db.Column(db.String(100), nullable=False) 

with app.app_context():
    db.create_all()


# =====================================================================
# Funtion sitess here, Create Funtion Here
# =====================================================================
            


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
    token = jwt.encode(payload , app.config['SECRET_KEY'] , algorithm='HS256')
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
        existing_email = User.query.filter_by(email=data['email']).first()      
        if existing_email:
            return jsonify({"status": "Error", "message": "Email Already Exists" }), 401
        else:
            is_pass = check_password(data["password"] , data["C_password"])
            if not is_pass:
                return jsonify({"status": "Error", "message": "Password Doesen't Match" }), 401
            else:
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = User(username=data['name'] , email=data['email'] , password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                new_id = new_user.id
                token = Create_token(new_id , data["name"])

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
        user = User.query.filter_by(email=email).first()
        if user:
            if user:
                typed_password_bytes = password.encode('utf-8')
        
                stored_hash_bytes = user.password.encode('utf-8')
        
                if bcrypt.checkpw(typed_password_bytes, stored_hash_bytes):  
                    id = user.id
                    token = Create_token(id , user.username)
                    return jsonify({"status": "success", 'token': token }), 200
                else:
                    return jsonify({"status":"error" , "message": "Password incorrect"}) , 401    
        else:
            return jsonify({"status":"error" , "message": "Either email or password is incorrect"}) , 401

            


 


# =====================================================================
# ROUTE 1: Login (Usually happens - Generates the Token + Extra Info)
# =====================================================================

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"status": "error", "message": "Token is missing!"}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        l_user = User.query.get(data['id'])
        return jsonify({
            "status": "success",
            "secret_data": f"Welcome {l_user.username}! Here is your highly secure data."
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired", "message": "Your session has expired. Please login again."}), 401
        
    except jwt.InvalidTokenError:
        return jsonify({"status": "error", "message": "Invalid token!"}), 401






if __name__ == '__main__':
    app.run(debug=True)


        





