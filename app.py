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
    return render_template("login-page.html", ip_addr=ip_addr)

@app.route('/itemlist')
def item():
    return render_template("item-list.html", ip_addr=ip_addr)

@app.route('/register')
def register_page():
    return render_template("register-page.html", ip_addr=ip_addr)


@app.route('/add_icecream_id/<icecream_id>', methods=['POST','GET'])
def add_icecream_id(icecream_id):
    iid = icecream_id
    c = icecream.find_one({"_id": int(iid)})
    return render_template("add-icecream.html", data=c, ip_addr=ip_addr)


@app.route('/register_icecreamsubmit', methods=['POST','GET'])
def register_icecreamsubmit():
    try:
        c = icecream.find_one(sort=[("_id", -1)])["_id"]
        c = c + 1
    except:
        c = 1

    icecream_name = request.form["icecream_name"]
    icecream_flavour = request.form["icecream_flavour"]
    icecream_type = request.form["icecream_type"]
    icecream_price = request.form["icecream_price"]
    description = request.form["description"]

    mydict = {'_id': c, 'icecream_name': icecream_name, 'icecream_flavour': icecream_flavour, 'icecream_type': icecream_type, 'icecream_price': icecream_price, 'description': description}
    y = icecream.insert_one(mydict)
    return render_template("item-list.html")


@app.route('/favorites', methods=['POST','GET'])
def add_favorites():

    c = request.form["uid"]
    icecream_name = request.form["icecream_name"]
    icecream_flavour = request.form["icecream_flavour"]
    icecream_type = request.form["icecream_type"]
    icecream_price = request.form["icecream_price"]
    description = request.form["description"]

    mydict = {'icecream_name': icecream_name, 'icecream_flavour': icecream_flavour, 'icecream_type':  icecream_type, ' icecream_price':  icecream_price, 'description': description}

    y = item.update_one({"_id" : int(c)}, {"$set": mydict}, upsert=False)
    return render_template("item-list.html")



@app.route('/all_icecream', methods=['GET'])
def all_icecream():
    cursor = item.find()
    l = []
    for document in cursor:
        l.append(document)
        print(l)
    data = {"item":l}
    ff = json.loads(json_util.dumps(data))
    return jsonify(ff)

@app.route('/logout')
def logout():
    return render_template("logout-page.html", ip_addr=ip_addr)

if __name__ == '__main__':
    #app.run(debug=True)
    print("IP Address :", ip_addr)
    app.run(debug=True, host='0.0.0.0')
