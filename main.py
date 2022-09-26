
from asyncio.windows_events import NULL
from msilib.schema import Binary
from flask import Flask, render_template,jsonify, request, session, flash, redirect, url_for, make_response
import pymongo
import certifi
import gridfs
from tkinter import Grid
import json

app = Flask(__name__)
app.secret_key = 'InternshipProject'

ca = certifi.where()

#database connection

client = pymongo.MongoClient("mongodb+srv://hetansh:h30@cluster0.zj9vapt.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.user

#imageStore = gridfs.GridFS(db)

@app.route("/updateImage", methods = ['GET', 'POST'])
def updateImage():
    if request.method == 'POST' and 'loggedin' in session:
        profileImage = request.files["image"]
        with open(profileImage, 'rb') as img:
            content = img.read()
        imageStore.put(content, filename = session['uemail'])
        return make_response("OK", 200)
    return make_response("Failed", 400)


#to register the users
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form["name"]
        uemail = request.form["email"]
        password = request.form["pass"]
        phone = request.form["phone"]
        bio = request.form["bio"]
        #profileImage = request.files["image"]
        if(len(list(db.users.find({"email":uemail}))) > 0):
            return make_response("Failed", 400)
        else:
            #with open(profileImage, 'rb') as img:
            #    content = img.read()
            #imageStore.put(content, filename = uemail)
            db.users.insert_one({"username":uname, "email":uemail, "password":password, "phone":phone , "bio":bio})
            return make_response("OK", 200)
    if 'loggedin' in session:
        return make_response("OK", 200)
    return make_response("Failed", 400)    

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and db is not None:
        uemail = request.form["email"]
        password = request.form["pass"]
        df = db.users.find_one({"email":uemail,"password":password})
        if df is not None:
            session['loggedin'] = True
            session['uemail'] = df["email"]
            return make_response("OK", 200)
        else :
            #flash("User Not Found")
            return make_response("Failed", 400)
    if 'loggedin' in session:
        return make_response(password, 200)
    return make_response("Failed", 400)

@app.route('/logout')
def logout() :
	session.pop('uemail', None)
	session.pop('loggedin', None)
	return make_response("OK", 200)

@app.route('/profile', methods = ['GET'])
def profile():
    #if 'loggedin' in session:
    df = db.users.find_one({"email":session['uemail']},{'_id': 0}) 
        # df[email]=email of user
        # df[username]=name of user
        #profileImage = imageStore.get_last_version(session['uemail']).read() # profileImage of user
    return df
    #return make_response("Failed", 400)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST' and 'loggedin' in session:
        uname = request.form["name"]
        uemail = request.form["email"]
        password = request.form["pass"]
        phone = request.form["phone"]
        bio = request.form["bio"]
        #profileImage = request.files["[--image--]"]
        #with open(profileImage, 'rb') as img:
            #   content = img.read()
        #imageStore.put(content, filename = uemail)
        db.users.update_one({"email":uemail},{"$set":{"username":uname, "email":uemail, "password":password,"phone":phone , "bio":bio}})
        return make_response("OK", 200)
    return make_response("Failed", 400)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST' and 'loggedin' in session:
        uemail = request.form["email"]
        db.users.delete_one({"email":uemail})
        return make_response("OK", 200)
    return make_response("Failed", 400)

@app.route("/")
def index():
    return 
    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)