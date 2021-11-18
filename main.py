####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, flash, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from __init__ import create_app, db

####################################################################
# our main blueprint
main = Blueprint('main', __name__)
####################################################################
@main.route('/') # home page that return 'index'
def index():
    return render_template("index.html")

####################################################################
@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

####################################################################
@main.route('/new-user') # page for new users to select plant type
@login_required
def new_user():
    if request.method == "POST":
        # update user's plant type here
        return redirect(url_for('main.profile'))

    return render_template('new_user.html')

####################################################################
app = create_app() # we initialize our flask app using the            
                   #__init__.py function
####################################################################
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode