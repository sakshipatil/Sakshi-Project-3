from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from flask import Flask,request, render_template, jsonify
from flask_cors import CORS
import time
from werkzeug import secure_filename
import imghdr
import  os
import socket
import json
from bson import json_util

client = MongoClient('mongodb://localhost:27017/')
mydb = client.icecreamDB
icecream = mydb.icecream

app = Flask(__name__)
api = Api(app)
CORS(app)

#To get IP Address
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
ip_addr="http://"+str(IP)+":5000/"


# route for home page
@app.route('/')
def login():
    return render_template("login-user.html", ip_addr=ip_addr)

@app.route('/register')
def register():
    return render_template("register-user.html", ip_addr=ip_addr)

@app.route('/icecreamlist')
def icecreamlist():
    return render_template("icecream-list.html", ip_addr=ip_addr)

@app.route('/addicecream')
def addicecream():
    return render_template("add-icecream.html", ip_addr=ip_addr)

@app.route('/add_icecream_id/<icecream_id>', methods=['POST','GET'])
def add_icecream_id(icecream_id):
    iid = icecream_id
    c = icecream.find_one({"_id": int(iid)})
    return render_template("add-icecream.html", data=c, ip_addr=ip_addr)

@app.route('/add_favorite_id/<favorite_id>', methods=['POST','GET'])
def add_favorite_id(icecream_id):
    iid = icecream_id
    c = icecream.find_one({"_id": int(iid)})
    return render_template("icecream-list.html", data=c, ip_addr=ip_addr)

@app.route('/edit_icecream_id/<icecream_id>', methods=['POST','GET'])
def edit_icecream_id(icecream_id):
    iid = icecream_id
    c = icecream.find_one({"_id": int(iid)})
    return render_template("edit-icecream.html", data=c,ip_addr=ip_addr)


@app.route('/favorite')
def addfavorite():
    return render_template("icecream-list.html", ip_addr=ip_addr)

@app.route('/all_icecream', methods=['GET'])
def all_icecream():
    cursor = icecream.find()
    l = []
    for document in cursor:
        l.append(document)
        print(l)
    data = {"item": l}
    ff = json.loads(json_util.dumps(data))
    return jsonify(ff)

@app.route('/logout')
def logout():
    return render_template("logout-page.html", ip_addr=ip_addr)

if __name__ == '__main__':
    #app.run(debug=True)
    print("IP Address :", ip_addr)
    app.run(debug=True, host='0.0.0.0')
