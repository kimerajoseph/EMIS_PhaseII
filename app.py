from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pymysql
import random
import os
#from python_scripts import app_variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT EXTERNAL SCRIPTS AND CONFIGS
from config import Config
from database import db
from models import User, SubstationNode, IPPNode, StandaloneNode
import store_data_to_db

# username=os.getenv("USER")
# password = os.getenv('PASSWORD')
# host=os.getenv("SERVER")
# database = os.getenv('DB_NAME')
# port=os.getenv("PORT")

app = Flask(__name__)
app.config.from_object(Config)
# #INITIALIASE AND CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
# #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.urandom(12).hex()
db.init_app(app)
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

if db:
    print("Connected to database")

# create connection for insertind data
# connection = pymysql.connect(host=host, user=username, password=password,database=database)
# cursor = connection.cursor()

# MODELS HERE

with app.app_context():
    db.create_all()  # Create database tables
    print("Database tables created")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/error', methods=['POST'])
def error():
    return render_template('home.html')

# ajax for populating dropdown
@app.route('/get_options', methods=['POST'])
def get_options():
    print("ajax called")
    category = request.json.get('category')  # Get category from request
    print("selected category: ",category)
    if category == 'Substation':
        data = ["Lugogo", "Mutundwe", "Kawanda", "Namanve", "Kapeeka"]
    elif category == 'IPP':
        data = ['Ziba', 'Kikagati', 'Nkenda', 'Siti', 'Kabulasoke']
    elif category == 'Standalone':
        data = ['Kasese', 'Kabale', 'Mbarara', 'Masaka', 'Mbale']
    return jsonify(data)  # Return as JSON

@app.route('/energy_meters', methods=['POST'])
def energy_meters():
    # connect to db and fetch existing nodes
    metering_nodes = ['']
    return render_template('energy_meter.html')

@app.route('/metering_node', methods=['POST'])
def metering_node():
    substations = ['Lugogo', 'Mutundwe', 'Kawanda', 'Namanve', 'Kapeeka']
    ipps = ['Sindila','Mahoma','Bugoye','KCCL']
    return render_template('metering_node.html', substations = substations, ipps=ipps)

@app.route('/store_metering_node', methods=['POST'])
def store_metering_node():
    form_data = request.form.to_dict()
    print(form_data)

    if(form_data['category'] != 'Standalone'):
        del form_data['distributor_2']
        form_data['distributor'] = form_data['distributor_1']
        del form_data['distributor_1']
        #print(form_data)
    
    my_message = store_data_to_db.store_node_data(form_data,db)
    return render_template('success.html', message=my_message)

# STORE ENERGY METER DATA
@app.route('/store_energy_meters', methods=['POST'])
def store_energy_meters():
    form_data = request.form.to_dict()
    print(form_data)
    #my_message="Data stored successfully"
    my_message = store_data_to_db.store_energy_meter_data(form_data,db)
    if my_message == "Data stored successfully":
        return render_template('success.html', message=my_message)
    else:
        return render_template('errors.html', message="record not stored. contact admin")

# store metering billing data   
@app.route('/monthly_billing_data_submission', methods=['POST'])
def monthly_billing_data_submission():
    form_data = request.form.to_dict()
    print(form_data)
    my_message=store_data_to_db.store_monthly_billing_data(form_data,db)
    if my_message == "Data stored successfully":
        return render_template('success.html', message=my_message)
    else:
        return render_template('errors.html', message="record not stored. contact admin")

# store substation data
@app.route('/substation_submission', methods=['POST'])
def substation_submission():
    form_data = request.form.to_dict()
    print(form_data)
    my_message=store_data_to_db.store_substation_data(form_data,db)

    if my_message == "Data stored successfully":
        return render_template('success.html', message=my_message)
    else:
        return render_template('errors.html', message="record not stored. contact admin")


# route to rende substations.html template. route name is  substation
@app.route('/substation', methods=['POST'])
def substation():
    return render_template('substations.html')

# User Registration
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return render_template('errors.html', message="Email already used. Please login or use another email")

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    my_message="Registration is successful"
    return render_template('success.html', message = my_message)

# User Login
@app.route('/login', methods=['POST'])
def login():
    print("function called")
    email = request.form['email']
    password = request.form['password']  
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        #my_message="logged in successfully"
        return render_template('home.html')
    else:
        print("user not found")
        return render_template('errors.html', message="user not found. check email or register first")


# Dashboard (Protected Route)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('home'))
    return "Welcome to your dashboard!"

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    # flash('You have been logged out.', 'info')
    # return redirect(url_for('home'))
    return render_template('index.html')

# API to get all substations
@app.route('/api/get_substations' , methods=['POST'])
def get_substations():
    substations = ['Lugogo', 'Mutundwe', 'Kawanda', 'Namanve', 'Kapeeka']
    return jsonify(substations)

# render metering billing data form
@app.route('/metering_form', methods=['POST'])
def metering_form():
    return render_template('meter_reading_form.html')


# metering billing data form validation
@app.route('/monthly_data_validation', methods=['POST'])
def metering_billing():
    # get meter_no, meter_type, cumulative_imports, cumulative_export, month, year from the DB
    meter_no = request.json.get('meter_no')  # Get category from request
    #meter_type = random.choice(['LG E650', 'A1700','A1800','CEWE Prometer','CEWE Prometer 100'])
    meter_type = random.choice(['LG E650', 'A1700'])
    print(meter_no)
    return jsonify({meter_no: meter_no,'cumulative_import':1290, 'cumulative_export':1100, 'meter_type':meter_type})  # Return as JSON


if __name__ == '__main__':
    app.run(debug=True)



