from flask import render_template, redirect, url_for, request, abort, Blueprint
from is_safe_url import is_safe_url
from flask_login import login_user, current_user, logout_user, login_required
from firebase_admin import auth as admin_auth
from app.config import login_manager, FIREBASE_CREDENTIALS, DOMAIN_NAME
from app.main.model import AboutDocList, ExpDocList, SkillDocList
from app.main.forms import ProfileForm
from time import sleep
main = Blueprint('main', __name__)




@main.route('/')
def index():
    return render_template('index.html',about_list = AboutDocList().about_list, exp_list = ExpDocList().exp_list, skill_list = SkillDocList().skill_list)


@main.route('/company')
def company():
    return render_template('cards/company.html')


#Login
@main.route("/login", methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == "POST":        #Only if data has been posted
        data = request.get_json()
        data = dict(data)
        sleep(0.1)
        print("got user")
        result = admin_auth.verify_id_token(data['stsTokenManager']['accessToken'])
        if result['uid'] == data['uid']:
            user = User(data)
            login_user(user, remember=True)
            return redirect(url_for('main.index'))
    next = request.args.get('next')
    if next:
        if not is_safe_url(next,('localhost','127.0.0.1',DOMAIN_NAME)):
            return abort(400)
    else:
        next = '/'
    return render_template("login.html",FIREBASE_CREDENTIALS=FIREBASE_CREDENTIALS, next=next)



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


@main.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    user = current_user
    if request.method == "POST":
        if form.validate_on_submit(): 
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.contact_email = form.contact_email.data
            user.phone = form.phone.data
            user.save_profile()
            alert = {'success':'Profile Updated.'}
            return render_template('forms/profile.html', form=form ,alert=alert) 
    else:
        print(user.first_name)
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.contact_email.data = user.contact_email
        form.phone.data = user.phone
    return render_template('forms/profile.html', form=form)