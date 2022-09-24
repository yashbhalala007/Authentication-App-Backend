from tkinter import Grid
from flask import Flask, render_template, request, session, flash, redirect, url_for, make_response
import pymongo
import certifi
import gridfs

app = Flask(__name__)
app.secret_key = 'InternshipProject'

ca = certifi.where()

#database connection
client = pymongo.MongoClient("mongodb+srv://assignment1:Assignment@internshipproject.wp4835d.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.user
imageStore = gridfs.GridFS(db)

@app.route("/updateImage", methods = ['GET', 'POST'])
def updateImage():
    if request.method == 'POST':
        profileImage = request.files["[--image--]"]
        with open(profileImage, 'rb') as img:
            content = img.read()
        imageStore.put(content, filename = uemail)
        return make_response("OK", 200)


#to register the users
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form["[--uname--]"]
        uemail = request.form["[--email--]"]
        password = request.form["[--pass--]"]
        profileImage = request.files["[--image--]"]
        if(len(list(db.users.find({"email":uemail}))) > 0):
            flash("User Already Exists")
            return make_response("Failed", 400)
        else:
            with open(profileImage, 'rb') as img:
                content = img.read()
            imageStore.put(content, filename = uemail)
            db.users.insert_one({"username":uname, "email":uemail, "password":password})
            return make_response("OK", 200)    

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)