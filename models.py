# models.py
from database import db

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Define the model (table structure)
class SubstationNode(db.Model):
    __tablename__ = 'substation_nodes'
    
    # Define columns
    substation = db.Column(db.String(255), nullable=False, primary_key=True)
    node_name = db.Column(db.String(255), nullable=False,primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    distributor = db.Column(db.String(255), nullable=False)
    voltage_level = db.Column(db.Integer(), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    remote_status = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<SubstationNode {self.substation} - {self.node_name}>"
    
# Define the model (table structure)
class IPPNode(db.Model):
    __tablename__ = 'ipp_nodes'
    
    # Define columns
    ipp_name = db.Column(db.String(255), nullable=False, primary_key=True)
    node_name = db.Column(db.String(255), nullable=False,primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    distributor = db.Column(db.String(255), nullable=False)
    voltage_level = db.Column(db.Integer(), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    classification = db.Column(db.String(255), nullable=False)
    remote_status = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<IPPNode {self.ipp} - {self.node_name}>"
    

class StandaloneNode(db.Model):
    __tablename__ = 'standalone_nodes'

    # Define columns
    #ipp = db.Column(db.String(255), nullable=False, primary_key=True)
    node_name = db.Column(db.String(255), nullable=False,primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    distributor1 = db.Column(db.String(255), nullable=False)
    distributor2 = db.Column(db.String(255), nullable=False)
    voltage_level = db.Column(db.Integer(), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    classification = db.Column(db.String(255), nullable=False)
    remote_status = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<StandaloneNode {self.node_name}>"
    


