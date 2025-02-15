from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

username=os.getenv("USER")
password = os.getenv('PASSWORD')
host=os.getenv("SERVER")
database = os.getenv('DB_NAME')
port=os.getenv("PORT")

app = Flask(__name__)
#INITIALIASE AND CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

if db:
    print("Connected to database")

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()  # Create database tables
    print("Database tables created")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/error', methods=['POST'])
def error():
    return render_template('index.html')

@app.route('/meters', methods=['POST'])
def process_form():
    form_data = request.form.to_dict()  # Get all form inputs as a dictionary
    return f"Received Data: {form_data}"

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
        # flash('Login successful!', 'success')
        # return redirect(url_for('dashboard'))
        my_message="logged in successfully"
        return render_template('success.html', message = my_message)
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

if __name__ == '__main__':
    app.run(debug=True)



