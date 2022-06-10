from flask import render_template, Blueprint
from flask_login import login_required
something = Blueprint('something', __name__)

@something.route('/awesome')
@login_required
def awesome():
    return render_template('awesome.html')    
