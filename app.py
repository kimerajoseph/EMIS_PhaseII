from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pymysql
import random
import os
#from flask_login import current_user, LoginManager, login_manager
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
#from python_scripts import app_variables
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()

# IMPORT EXTERNAL SCRIPTS AND CONFIGS
from config import Config
from database import db
from models import User, SubstationNode, IPPNode, StandaloneNode
import store_data_to_db, ajax_calls, store_data_from_files

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

login_manager = LoginManager()
login_manager.init_app(app)

# Folder to store uploaded files
UPLOAD_FOLDER = 'File_Uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set allowed extensions for security reasons
ALLOWED_EXTENSIONS = {'xls', 'csv','xlsx'}

# Configure Flask-Mail (set these in your app config)
mail = Mail(app)

def generate_otp():
    return str(random.randint(100000, 999999))

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if db:
    print("Connected to database")

# create connection for insertind data
# connection = pymysql.connect(host=host, user=username, password=password,database=database)
# cursor = connection.cursor()

# MODELS HERE
with app.app_context():
    db.create_all()  # Create database tables
    print("Database tables created")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/error', methods=['POST'])
@login_required
def error():
    return render_template('index.html')

# ajax for populating dropdown
@app.route('/get_options', methods=['POST'])
def get_options():
    print("ajax called")
    category = request.json.get('category')  # Get category from request
    print("selected category: ",category)
    if category == 'Substation':
        data = ajax_calls.get_substations()
        return jsonify(data)  # Return as JSON
    elif category == 'IPP':
        #data = ['Ziba', 'Kikagati', 'Nkenda', 'Siti', 'Kabulasoke']
        data = ajax_calls.get_ipps()
        return jsonify(data)  # Return as JSON
    elif category == 'Standalone':
        data = []
        return jsonify(data)  # Return as JSON
    
# ajax for updating node or substation options for energy meter form
@app.route('/get_node_options', methods=['POST'])
def get_node_options():
    print("ajax called")
    category = request.json.get('category')  # Get category from request
    print("selected category: ",category)
    if category == 'Substation':
        data = ajax_calls.get_substations()
        return jsonify(data)  # Return as JSON
    elif category == 'IPP':
        #data = ['Ziba', 'Kikagati', 'Nkenda', 'Siti', 'Kabulasoke']
        data = ajax_calls.get_ipps()
        return jsonify(data)  # Return as JSON
    elif category == 'Standalone':
        data = ajax_calls.get_standalones()
        return jsonify(data)  # Return as JSON
    

# UPDATE SUBSTATIONS AND IPPS NODES
@app.route('/get_ipp_substation_nodes', methods=['POST'])
def get_ipp_substation_nodes():
    print("ajax called")
    ipp_substation = request.json.get('ipp_substation')  # Get category from request
    category = request.json.get('category')  # Get category from request
    print("selected category: ",ipp_substation)
    if category == 'Substation':
        data = ajax_calls.get_substation_nodes(ipp_substation)
        return jsonify(data)  # Return as JSON
    elif category == 'IPP':
        #data = ['Ziba', 'Kikagati', 'Nkenda', 'Siti', 'Kabulasoke']
        data = ajax_calls.get_ipp_nodes(ipp_substation)
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
@login_required
def store_metering_node():
    form_data = request.form.to_dict()
    print(form_data)

    if(form_data['category'] != 'Standalone'):
        del form_data['distributor_2']
        form_data['distributor'] = form_data['distributor_1']
        del form_data['distributor_1']
        #print(form_data)
    
    my_message = store_data_to_db.store_node_data(form_data,db)
    if my_message == "Data stored successfully":
        return render_template('success.html', message=my_message)
    else:
        return render_template('errors.html', message="record not stored. contact admin")

# STORE ENERGY METER DATA
@app.route('/store_energy_meters', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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


@app.route('/ipps_form', methods=['POST'])
def ipps_form():
    return render_template('ipps_form.html')

# store ipps data
@app.route('/ipps_submission', methods=['POST'])
def ipps_submission():
    form_data = request.form.to_dict()
    print(form_data)
    my_message=store_data_to_db.store_ipp_data(form_data,db)

    if my_message == "Data stored successfully":
        return render_template('success.html', message=my_message)
    else:
        return render_template('errors.html', message="record not stored. contact admin")
    
# process data from files
# Route to handle file upload
@app.route('/submit_files', methods=['POST'])
@login_required
def submit_files():
    #print("function for files called")
    files_sent = request.files['fileInput']
    data = request.form.to_dict()    
    print("file is : ", files_sent.filename)
    #current_user = user.name
    files_paths = []
    # save file to server
    if files_sent and allowed_file(files_sent.filename) and len(request.files.getlist("fileInput")) == 1:
        filename = files_sent.filename
        manufacturer_folder = os.path.join(UPLOAD_FOLDER, data['meterTypeFile'])
        os.makedirs(manufacturer_folder, exist_ok=True) 
        file_path = os.path.join(manufacturer_folder, filename)
        # Save the file
        files_sent.save(file_path)

        if data['meterTypeFile'] == "LGE650":             
            my_message = store_data_from_files.process_landis_data(db,file_path,filename,data)
            if my_message == "Data stored successfully":
                return render_template('success.html', message = my_message)
        
        elif len(request.files.getlist("fileInput")) == 1 and data['meterTypeFile'] == "Elster A1700":             
            my_message = store_data_from_files.process_Elster_data(db,file_path,filename,data)
            if my_message == "Data stored successfully":
                return render_template('success.html', message = my_message)

    # FOR PROMETER AND PROMETER 100 save file to server
    elif files_sent and allowed_file(files_sent.filename) and len(request.files.getlist("fileInput")) == 2:   
        file_list = request.files.getlist("fileInput")
        for file in file_list:
            filename = file.filename.strip()
            manufacturer_folder = os.path.join(UPLOAD_FOLDER, data['meterTypeFile'])
            os.makedirs(manufacturer_folder, exist_ok=True) 
            file_path = os.path.join(manufacturer_folder, filename)
            # Save the file
            file.save(file_path)
            files_paths.append(file_path)
        print(files_paths)

        if data['meterTypeFile'] == "CEWE Prometer 100": 
            my_message = store_data_from_files.process_pro100_data(db,files_paths,filename,data)
            if my_message == "Data stored successfully":
                return render_template('success.html', message = my_message)
            
        elif data['meterTypeFile'] == "CEWE Prometer": 
            my_message = store_data_from_files.process_prometer_data(db,files_paths,filename,data)
            if my_message == "Data stored successfully":
                return render_template('success.html', message = my_message)

   
        
    # elif len(request.files.getlist("fileInput")) == 2 and data['meterTypeFile'] == "CEWE Prometer 100":             
    #     my_message = store_data_from_files.process_pro100_data(db,file_path,filename,data)
    #     if my_message == "Data stored successfully":
    #         return render_template('success.html', message = my_message)


# User Registration
# @app.route('/register', methods=['POST'])
# def register():
#     name = request.form['name']
#     email = request.form['email']
#     password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return render_template('errors.html', message="Email already used. Please login or use another email")

#     new_user = User(name=name, email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     my_message="Registration is successful"
#     return render_template('success.html', message = my_message)

@app.route('/register', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    if User.query.filter_by(email=email).first():
        return render_template('errors.html', message="Email already registered.")

    otp = generate_otp()
    user = User(email=email, password=password, otp=otp, is_verified=False, name=name)
    db.session.add(user)
    db.session.commit()

    # Send OTP via email
    msg = Message("Your OTP Verification Code", sender="jkimera5@gmail.com", recipients=[email])
    msg.body = f"Your OTP is {otp}"
    mail.send(msg)

    return render_template('verify_otp.html', email=email)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email = request.form['email']
    input_otp = request.form['otp']

    user = User.query.filter_by(email=email).first()
    if user and user.otp == input_otp:
        user.is_verified = True
        user.otp = None
        db.session.commit()
        return render_template('index.html', message="Email verified. You may now log in.")
    else:
        return render_template('verify_otp.html', email=email, message="Invalid OTP. Try again.")


# User Login
# @app.route('/login', methods=['POST'])
# def login():
#     #print("function called")
#     email = request.form['email']
#     password = request.form['password']  
#     user = User.query.filter_by(email=email).first()

#     if user and bcrypt.check_password_hash(user.password, password):
#         login_user(user)
#         #print(user.name, user.email)
#         return render_template('home.html', current_user = user )
#     else:
#         #print("user not found")
#         return render_template('errors.html', message="user not found. check email or register first")

@app.route('/login', methods=['POST']) 
def login():
    email = request.form['email']
    password = request.form['password']  
    user = User.query.filter_by(email=email).first()

    if not user:
        return render_template('errors.html', message="User not found. Check email or register first")

    if not user.is_verified:
        return render_template('errors.html', message="Please verify your email before logging in.")

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return render_template('home.html', current_user=user)
    else:
        return render_template('errors.html', message="Incorrect password.")



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
    #session.pop('user_id', None)
    logout_user()
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

# get all meter numbers 
@app.route('/get_meter_numbers', methods=['POST'])
def get_meter_numbers():
    #meter_numbers = ['MTR-001', 'MTR-002', 'MTR-003', 'MTR-004', 'MTR-005']
    meter_numbers = ajax_calls.get_meter_numbers(db)
    return jsonify(meter_numbers)




if __name__ == '__main__':
    app.run(debug=True)



