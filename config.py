import os
from dotenv import load_dotenv
load_dotenv()

username=os.getenv("USER")
password = os.getenv('PASSWORD')
host=os.getenv("SERVER")
database = os.getenv('DB_NAME')
port=os.getenv("PORT")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    SECRET_KEY = os.urandom(12).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


