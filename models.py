# models.py
from database import db
from sqlalchemy import Enum
import uuid
from flask_login import UserMixin

# User Model
class User(db.Model,UserMixin):
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
        return f"<IPPNode {self.ipp_name} - {self.node_name}>"
    

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
    

class energyMeters(db.Model):
    __tablename__ = 'energy_meters'

    # Define columns
    serial_no = db.Column(db.String(255), nullable=False, primary_key=True)
    meter_category = db.Column(db.String(255), nullable=False)
    sub_ipp_name = db.Column(db.String(255), nullable=False)
    node_name = db.Column(db.String(255), nullable=False)
    meter_classification = db.Column(db.String(255), nullable=False)    
    manufacturer = db.Column(db.String(255), nullable=False)
    meter_type = db.Column(db.String(255), nullable=False)
    YOM = db.Column(db.String(255), nullable=False)
    accuracy = db.Column(db.String(255), nullable=False)
    meter_usage = db.Column(db.String(255), nullable=False)
    no_of_elements = db.Column(db.String(255), nullable=False)
    CT_ratio = db.Column(db.String(255), nullable=False)
    VT_ratio = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<energyMeters {self.serial_no}>"
    

#MONTHLY DATA
class monthlyBillingData(db.Model):
    __tablename__ = 'monthly_billing_data'

    # Define columns
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    serial_no = db.Column(db.String(255), nullable=False)
    meter_category = db.Column(db.String(255), nullable=False)
    node_name = db.Column(db.String(255), nullable=False)
    billing_period = db.Column(db.Date, nullable=False)    
    reading_date = db.Column(db.DateTime, nullable=False)
    cumulative_import = db.Column(db.Numeric(15, 2), nullable=False)
    cumulative_export = db.Column(db.Numeric(15, 2), nullable=False)
    rate1 = db.Column(db.Numeric(15, 2), nullable=False)
    rate2 = db.Column(db.Numeric(15, 2), nullable=False)
    rate3 = db.Column(db.Numeric(15, 2), nullable=False)
    rate4 = db.Column(db.Numeric(15, 2), nullable=False)
    rate5 = db.Column(db.Numeric(15, 2), nullable=False)
    rate6 = db.Column(db.Numeric(15, 2), nullable=False)
    max_dem1 = db.Column(db.Numeric(15, 2), nullable=False)
    max_dem1_datatime = db.Column(db.DateTime, nullable=False)
    max_dem2 = db.Column(db.Numeric(15, 2), nullable=False)
    max_dem2_datatime = db.Column(db.DateTime, nullable=False)
    max_dem3 = db.Column(db.Numeric(15, 2), nullable=False)
    max_dem3_datatime = db.Column(db.DateTime, nullable=False)
    reactive_import = db.Column(db.Numeric(15, 2), nullable=False)
    reactive_export = db.Column(db.Numeric(15, 2), nullable=False)
    apparent_import = db.Column(db.Numeric(15, 2), nullable=False)
    no_of_resets = db.Column(db.Integer(), nullable=False)
    date_of_last_reset = db.Column(db.DateTime, nullable=False)
    programing_count = db.Column(db.Integer(), nullable=False)
    CT_ratio = db.Column(db.String(255), nullable=False)
    VT_ratio = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<monthly_billing_data {self.serial_no}>"
    



class Substation(db.Model):
    __tablename__ = 'substations'

    # Define columns
    name = db.Column(db.String(255), nullable=False, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    no_of_nodes = db.Column(db.Integer(), nullable=False)
    billing_nodes = db.Column(db.Integer(), nullable=False)
    energy_loss_nodes = db.Column(db.Integer(), nullable=False)
    manned = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<Substation {self.name}>"
    
class IPP(db.Model):
    __tablename__ = 'ipps'

    # Define columns
    name = db.Column(db.String(255), nullable=False, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    no_of_billing_nodes = db.Column(db.Integer(), nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # String representation for easy debugging
    def __repr__(self):
        return f"<IPP {self.name}>"