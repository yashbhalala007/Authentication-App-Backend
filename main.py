from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from asyncio.windows_events import NULL
from msilib.schema import Binary
from flask import Flask, render_template,jsonify, request, session, flash, redirect, url_for, make_response
import pymongo
from PIL import Image
import certifi
import gridfs
import io
from tkinter import Grid
import json
from flask_cors import CORS
import matplotlib.pyplot as plt


app = Flask(__name__)
CORS(app)
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
        
        if(len(list(db.users.find({"email":uemail}))) > 0):
            return make_response("Failed", 400)
        else:
            #with open(profileImage, 'rb') as img:
            #    content = img.read()
            #imageStore.put(content, filename = uemail)
            db.users.insert_one({"username":uname, "email":uemail, "password":password, "phone":phone})
            db.image.insert_one({"email":uemail})
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
            return make_response("ok", 200)
    return make_response("Failed", 400)

@app.route('/logout')
def logout() :
	session.pop('uemail', None)
	session.pop('loggedin', None)
	return make_response("OK", 200)

@app.route('/profile', methods = ['GET','POST'])
def profile():
    if request.method == 'POST' and db is not None:
        uemail = request.form["email"]
        df = db.users.find_one({"email":uemail},{'_id': 0}) 
    #img=db.image.find_one({"email":session["uemail"]})
    #pil_img = Image.open(io.BytesIO(img['image']))
    # plt.imshow(pil_img)
    # plt.show()

        # df[email]=email of user
        # df[username]=name of user
        #profileImage = imageStore.get_last_version(session['uemail']).read() # profileImage of user
        return df
    #return make_response("Failed", 400)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        uname = request.form["name"]
        uemail = request.form["email"]
        password = request.form["pass"]
        phone = request.form["phone"]
        bio = request.form["bio"]
        profileImage = request.files["image"]
        pi = Image.open(profileImage)
        image_bytes = io.BytesIO()
        pi.save(image_bytes, format='JPEG')

        image = {
            'data': image_bytes.getvalue()
        }
        #with open(profileImage, 'rb') as img:
            #   content = img.read()
        #imageStore.put(content, filename = uemail)
        db.users.update_one({"email":uemail},{"$set":{"username":uname, "email":uemail, "password":password,"phone":phone , "bio":bio}})
        db.image.update_one({"email":uemail},{"$set":{"email":uemail, "image":image['data']}})
        return make_response("OK", 200)
    return make_response("Failed", 400)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST' and db is not None:
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