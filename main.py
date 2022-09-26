
from flask import Flask, render_template, request, session, flash, redirect, url_for, make_response
import pymongo
import certifi
import gridfs
from tkinter import Grid

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
        imageStore.put(content, filename = session['uemail'])
        return make_response("OK", 200)


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
            flash("User Already Exists")
            return make_response("Failed", 400)
        else:
            #with open(profileImage, 'rb') as img:
            #    content = img.read()
            #imageStore.put(content, filename = uemail)
            db.users.insert_one({"username":uname, "email":uemail, "password":password, "phone":phone , "bio":bio})
            return make_response("OK", 200)
    return make_response("Failed", 400)    

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
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
        return make_response("OK", 200)
    return make_response("Failed", 400)

@app.route('/logout')
def logout() :
	session.pop('uemail', None)
	session.pop('loggedin', None)
	return make_response("OK", 200)

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        df = db.users.find_one({"email":session['uemail']}) 
        # df[email]=email of user
        # df[username]=name of user
        profileImage = imageStore.get_last_version(session['uemail']).read() # profileImage of user
        return make_response("OK", 200)
    return make_response("Failed", 400)

@app.route('/update')
def update():
    if 'loggedin' in session:
        if request.method == 'POST':
            uname = request.form["[--uname--]"]
            uemail = request.form["[--email--]"]
            password = request.form["[--pass--]"]
            phone = request.form["[--phone--]"]
            bio = request.form["[--bio--]"]
            profileImage = request.files["[--image--]"]
            with open(profileImage, 'rb') as img:
                content = img.read()
            imageStore.put(content, filename = uemail)
            db.users.update_one({"email":session['uemail']},{"$set":{"username":uname, "email":uemail, "password":password,"phone":phone , "bio":bio}})
            return make_response("OK", 200)
    return make_response("Failed", 400)


@app.route("/")
def index():
    return 
    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)