# Building atop the simple example from https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
from flask import Flask, render_template, redirect, request, session
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session
import pickle 
 
app = Flask(__name__, template_folder='.')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

class UserData:
    def __init__(self, uname) -> None:
        self.file = None
        self.uname = uname
    def set_file(self, file):
        self.file = file
     
 
@app.route("/")
def index():
    nm = session.get("name")
    if not nm:
        return redirect("/login")
    else:   
        with open(f'./flask-session-test/pickles/{nm}', 'rb') as f:     
            ud = pickle.load(f)
    return render_template('index.html', context=ud)
 
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nm = request.form.get("name")
        uf = request.files['ufile'].filename
        ud = UserData(nm)
        ud.set_file(uf)
        session["name"] = nm
        with open(f'./flask-session-test/pickles/{nm}', 'wb') as f:
            pickle.dump(ud, f)
        return redirect("/")
    return render_template("login.html")
 
 
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
 
 
if __name__ == "__main__":
    app.run(debug=True)