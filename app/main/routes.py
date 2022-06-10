from flask import render_template, redirect, url_for, request, abort, Blueprint
from is_safe_url import is_safe_url
from flask_login import login_user, current_user, logout_user, login_required
from firebase_admin import auth as admin_auth
from app.config import login_manager, FIREBASE_CREDENTIALS, DOMAIN_NAME, GOOGLE_CLIENT_ID
from app.main.model import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')



#Login
@main.route("/login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == "POST":        #Only if data has been posted
        data = request.get_json()
        data = dict(data)
        result = admin_auth.verify_id_token(data['stsTokenManager']['accessToken'])
        if result['uid'] == data['uid']:
            user = User(data)
            login_user(user, remember=True)
            return redirect(url_for('main.index'))
    next = request.args.get('next')
    if next:
        if not is_safe_url(next,('127.0.0.1','localhost',DOMAIN_NAME)):
            return abort(400)
    else:
        next = '/'
    return render_template("login.html",FIREBASE_CREDENTIALS=FIREBASE_CREDENTIALS, GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID, next=next)



#Logout
@main.route("/logout")
def logout():
    logout_user()
    alert = {'success':'You have signed out.'}
    return render_template('index.html',alert=alert)   


#Login Manager
@login_manager.user_loader
def load_user(token):
    return User.get_user(token)
