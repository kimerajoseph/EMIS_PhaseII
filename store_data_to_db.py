from models import IPPNode, SubstationNode, StandaloneNode, energyMeters,monhtlyBillingData

def store_node_data(form_data,db):
    if(form_data['category'] == 'IPP'):
        new_node = IPPNode(
        ipp_name=form_data['ippName'],
        node_name=form_data['node_name'],
        location=form_data['location'],
        distributor=form_data['distributor'],
        voltage_level= form_data['voltageLevel'],
        region=form_data['region'],
        classification=form_data['type'],
        remote_status=form_data['remote']
        )
        
        # Add the object to the session and commit the transaction
        db.session.add(new_node)
        db.session.commit()
        #my_message="Data stored successfully"
        return "Data stored successfully"
    
    elif(form_data['category'] == 'Substation'):
        new_node = SubstationNode(
            substation=form_data['uetclSubstation'],
            node_name=form_data['node_name'],
            location=form_data['location'],
            distributor=form_data['distributor'],
            voltage_level= form_data['voltageLevel'],
            region=form_data['region'],
            category=form_data['category'],
            remote_status=form_data['remote']
        )
        
        # Add the object to the session and commit the transaction
        db.session.add(new_node)
        db.session.commit()
        #my_message="Data stored successfully"
        return "Data stored successfully"
    
    elif(form_data['category'] == 'Standalone'):
        new_node = StandaloneNode(
            #substation=form_data['uetclSubstation'],
            node_name=form_data['node_name'],
            location=form_data['location'],
            distributor1=form_data['distributor_1'],
            distributor2=form_data['distributor_2'],
            voltage_level= form_data['voltageLevel'],
            region=form_data['region'],
            classification=form_data['type'],
            remote_status=form_data['remote']
        )
        # Add the object to the session and commit the transaction
        db.session.add(new_node)
        db.session.commit()
        #my_message="Data stored successfully"
        return "Data stored successfully"
    
def store_energy_meter_data(form_data,db):
    new_energy_meter = energyMeters(
            
    # Define columns
    serial_no = form_data['serial_no'],
    meter_category = form_data['meter_category'],
    node_name = form_data['nodeName'],
    meter_classification = form_data['meter_classification'],
    manufacturer = form_data['manufacturer'],
    meter_type = form_data['meter_type'],
    YOM = form_data['YOM'],
    accuracy = form_data['accuracy'],
    meter_usage = form_data['meter_usage'],
    no_of_elements = form_data['no_of_elements'],
    CT_ratio = form_data['CT_ratio'],
    VT_ratio = form_data['VT_ratio']

    
    )
    # Add the object to the session and commit the transaction
    db.session.add(new_energy_meter)
    db.session.commit()
    #my_message="Data stored successfully"
    return "Data stored successfully"

# STORE MONTHLY BILLING DATA
def store_monthly_billing_data(form_data,db):
    new_billing_data = monhtlyBillingData(
            
    # Define columns    
    meter_category = form_data['meterCategory'],
    node_name = form_data['nodeName'],
    billing_period = form_data['billingPeriod'],
    serial_no = form_data['serialNo'],
    reading_date = form_data['DateTimeOfReading'],
    cumulative_import = form_data['CumulativeImport'],
    cumulative_export = form_data['CumulativeExport'],
    rate1 = form_data['Rate1'],
    rate2 = form_data['Rate2'],
    rate3 = form_data['Rate3'],
    rate4 = form_data['Rate4'],
    rate5 = form_data['Rate5'],
    rate6 = form_data['Rate6'],
    max_dem1 = form_data['MaxDem1'],
    max_dem1_datatime = form_data['MaxDem1DateTime'],
    max_dem2 = form_data['MaxDem2'],
    max_dem2_datatime = form_data['MaxDem2DateTime'],
    max_dem3 = form_data['MaxDem3'],
    max_dem3_datatime = form_data['MaxDem3DateTime'],
    reactive_import = form_data['ReactiveImport'],
    reactive_export = form_data['ReactiveExport'],
    apparent_import = form_data['ApparentImport'],
    no_of_resets = form_data['NumberOfResets'],
    date_of_last_reset = form_data['DateOfLastReset'],
    programing_count = form_data['ProgrammingCount'],
    CT_ratio = form_data['CTRatio'],
    VT_ratio = form_data['VTRatio'],
    
    )
    # Add the object to the session and commit the transaction
    db.session.add(new_billing_data)
    db.session.commit()
    #my_message="Data stored successfully"
    return "Data stored successfully"
    
