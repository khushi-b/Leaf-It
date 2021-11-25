####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, flash, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from flask_migrate import Migrate
from werkzeug.utils import redirect
from __init__ import create_app, db
from models import Plant
from moisture_readings import moisture_levels, last_watered
import os
####################################################################
# our main blueprint
main = Blueprint('main', __name__)

####################################################################
@main.route('/') # home page that return 'index'
def index():
    image = url_for('static', filename=f"backgroundImg.png") 
    return render_template("index.html", image=image)

####################################################################
@main.route('/profile', methods=['GET']) # profile page that return 'profile'
@login_required
def profile():
    # update moisture and last_watered data
    last_watered()
    moisture_levels()

    plant = Plant.query.filter_by(user_id=current_user.id).first()
    moisture_level = plant.moisture_level
    last_watered_value = plant.last_watered.strftime("%d/%m/%Y %H:%M:%S")
    plant_type = plant.plant_type.lower()

    # get plant image
    if plant.set_profile:
        print("set_profile")
        image = url_for('static', filename=f"plant_images/plant_{current_user.id}") 
    else:
        print("placeholder")
        image = url_for('static', filename=f"{plant.plant_type}.jpg")

    # get audio files for user
    recordings = []
    if plant.audio_count != None:
        for i in range(plant.audio_count):
            recordings.append(url_for('static', filename=f"audio/plant_{current_user.id}_{i}.wav"))

    return render_template('plant_status.html', name=current_user.name, moisture_level=moisture_level, last_watered=last_watered_value, image=image, recordings=recordings, plant=plant_type)

@main.route('/profile', methods=['POST'])
def upload_file():
    # plant image
    try:
        image = request.files['image_file']
        if image.filename != '':
            image.save(os.path.join("./static/plant_images", f"plant_{current_user.id}"))
            user_file = open(f"user_{current_user.id}", "w+")
            user_file.write("set_profile:True\n")
            user_file.close()
    except:
        pass
    
    # audio
    try:
        plant = Plant.query.filter_by(user_id=current_user.id).first()
        audio = request.files['audio_file']
        audio.save(os.path.join("./static/audio", f"plant_{current_user.id}_{plant.audio_count}.wav"))
        plant.audio_count += 1
        db.session.add(plant)
        db.session.commit()
    except:
        pass

    return redirect(url_for('main.profile'))

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
    return render_template('new_user.html')

####################################################################
app = create_app() # we initialize our flask app using the            
                   #__init__.py function
migrate = Migrate(app, db)
####################################################################
if __name__ == '__main__':
    db.create_all(app = create_app()) # create the SQLite database
    app.run(host="0.0.0.0",port="80",debug=True) # run the flask app on debug mode