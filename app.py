from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from flask import Flask,request, render_template, jsonify
from flask_cors import CORS
import time
import imghdr
import  os
import socket
import json
from bson import json_util

client = MongoClient('mongodb://localhost:27017/')
mydb = client.icecreamDB

icecream = mydb["icecream"]
mycols = mydb["user"]
favorites = mydb['favorites']

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

@app.route("/login_submit", methods=["POST"])
def login_submit():
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    login_sumbit = mycols.find_one({'username': username, 'password': password})
    if login_sumbit:
        return render_template('item-list.html', username=username)
    return "Invalid Username or Password"

@app.route("/register_submit",methods=["POST"])
def register_submit():
    if request.method == 'POST':
        Firstname = request.form['first_name']
        Lastname = request.form['last_name']
        Username = request.form['username']
        Password = request.form['password']
        print(Firstname, Lastname, Username, Password)

        existing_user = mycols.find_one({'username' : Username})
        existing_user = mycols.find_one({'username' : Username})

        if existing_user is None:
            mycols.insert({'first_name':Firstname,'last_name':Lastname,'username' : Username,'password' : Password})
            return render_template('submit.html')
        return 'That user Already Exists'
    return render_template('register-page.html')

@app.route('/register')
def register_page():
    return render_template("register-page.html", ip_addr=ip_addr)

@app.route('/addicecream')
def addicecream():
    return render_template("add-icecream.html", ip_addr=ip_addr)

@app.route('/submit')
def submit_page():
    return render_template("submit.html", ip_addr=ip_addr)

@app.route('/add_favorites_id/<icecream_id>', methods=['POST', 'GET'])
def add_icecream_id(icecream_id):
    iid = icecream_id
    c = icecream.find_one({"_id": int(iid)})
    print(c)
    favorites.insert(c)
    return render_template("item-list.html", ip_addr=ip_addr)

@app.route('/remove_favorites_id/<icecream_id>', methods=['POST', 'GET'])
def remove_icecream_id(icecream_id):
    iid = icecream_id
    c = icecream.find_one({"_id": int(iid)})
    print(c)
    favorites.remove(c)
    return render_template("item-list.html", ip_addr=ip_addr)

# @app.route('/edit_icecream_id/<icecream_id>', methods=['POST','GET'])
# def edit_icecream_id(icecream_id):
#     iid = icecream_id
#     c = icecream.find_one({"_id": int(iid)})
#     return render_template("edit-icecream.html", data=c,ip_addr=ip_addr)

@app.route('/add_icecreamsubmit', methods=['POST'])
def add_icecreamsubmit():
    try:
        c = icecream.find_one(sort=[("_id", -1)])["_id"]
        c = c + 1
    except:
        c = 1

    icecream_name = request.form["icecream_name"]
    icecream_flavour = request.form["icecream_flavour"]
    icecream_type = request.form["icecream_type"]
    icecream_price = request.form["icecream_price"]


    mydict = {'_id': c, 'icecream_name':  icecream_name, 'icecream_flavour': icecream_flavour, 'icecream_type': icecream_type, 'icecream_price': icecream_price}
    y = icecream.insert_one(mydict)
    return render_template("item-list.html")


@app.route('/favorites', methods=['POST', 'GET'])
def add_favorites():

    c = request.form["uid"]
    icecream_name = request.form["icecream_name"]
    icecream_flavour = request.form["icecream_flavour"]
    icecream_type = request.form["icecream_type"]
    icecream_price = request.form["icecream_price"]


    mydict = {'_id':c,'icecream_name': icecream_name, 'icecream_flavour': icecream_flavour, 'icecream_type':  icecream_type, ' icecream_price':  icecream_price}

    y = item.update_one({"_id" : int(c)}, {"$set": mydict}, upsert=False)
    return render_template("item-list.html")


@app.route('/all_icecream', methods=['GET'])
def all_icecream():
    cursor = icecream.find()
    l = []
    for document in cursor:
        print("D",document)
        l.append(document)
        print(l)
    data = {"item": l}
    print("DDDDDDDDDDDDDDDDD0",data)
    ff = json.loads(json_util.dumps(data))
    return jsonify(ff)

@app.route('/all_favorites_icecream', methods=['GET'])
def all_favorites_icecream():
    cursor = favorites.find()
    l = []
    for document in cursor:
        print("D",document)
        l.append(document)
        print(l)
    data = {"item": l}
    print("DDDDDDDDDDDDDDDDD0",data)
    ff = json.loads(json_util.dumps(data))
    return jsonify(ff)

@app.route('/logout')
def logout():
    return render_template("logout-page.html", ip_addr=ip_addr)

if __name__ == '__main__':
    #app.run(debug=True)
    print("IP Address :", ip_addr)
    app.run(debug=True, host='0.0.0.0')
