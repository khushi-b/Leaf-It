####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, flash, request
# Import for Migrations
from flask_migrate import Migrate, current
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from __init__ import create_app, db
from models import Plant
from moisture_readings import moisture_levels
from moisture_readings import last_watered
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
    last_watered()
    moisture_levels()
    plant = Plant.query.filter_by(user_id=current_user.id).first()
    moisture_level = plant.moisture_level
    #moisture_level = moisture_levels
    last_watered_value = plant.last_watered
    #last_watered = last_watered
    print(moisture_level)
    print(last_watered_value)
    return render_template('plant_status.html', name=current_user.name, moisture_level=moisture_level, last_watered=last_watered_value)

####################################################################
@main.route('/new-user', methods=['GET', 'POST']) # page for new users to select plant type
def new_user():
    if request.method == "POST":
        user_id = current_user.id
        plant = Plant(user_id = user_id, plant_type=request.values.get("plant_type"))
        db.session.add(plant)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('main.profile'))
    print("here")
    return render_template('new_user.html')

####################################################################
app = create_app() # we initialize our flask app using the            
                   #__init__.py function
####################################################################
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode

# Settings for migrations
migrate = Migrate(app, db)