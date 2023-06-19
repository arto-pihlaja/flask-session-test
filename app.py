# Building atop the simple example from https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
from flask import Flask, render_template, redirect, request, session
# The Session instance is not used for direct access, you should always use flask.session
#from flask_session import Session
from werkzeug.utils import secure_filename
import pickle 
import os
from uuid import uuid4 

if os.path.exists('./pickles'):
    pass
else:
    os.makedirs('./pickles')

app = Flask(__name__, template_folder='.')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'DefineLytcheSala'
#Session(app)

class UserData:
    def __init__(self, uname) -> None:
        self.file = None
        self.uname = uname
    def set_file(self, file):
        self.file = file
     
 
@app.route("/")
def index():
    ss = session._get_current_object()
    uid = session.get("uid")
    # Flask sessions expire when the browser is closed, which is fine https://flask.palletsprojects.com/en/2.3.x/api/#flask.session.permanent
    if not uid:
        return redirect("/login")
    else:           
        with open(os.path.join('./pickles', str(uid)), 'rb') as f:     
            ud = pickle.load(f)            
    return render_template('index.html', ud=ud, sid=str(uid))
 
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":        
        nm = request.form.get("name")
        uf = request.files['ufile'].filename
        ud = UserData(nm)
        ud.set_file(uf)
        uid = uuid4()
        session["uid"] = uid
        with open(os.path.join('./pickles', str(uid)), 'wb') as f:
            pickle.dump(ud, f)
        return redirect("/")
    return render_template("login.html")
 
 
@app.route("/logout")
def logout():
    session.pop('uid', default=None)     
    return redirect("/")
 
 
if __name__ == "__main__":
    app.run(debug=True)