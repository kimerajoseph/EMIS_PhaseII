from models import IPPNode, SubstationNode, StandaloneNode, energyMeters,monthlyBillingData,Substation,IPP

def store_node_data(form_data, db):
    if form_data['category'] == 'IPP':
        # Check if the node already exists by 'ipp_name' (or 'node_name' depending on the field you want to use for uniqueness)
        existing_node = IPPNode.query.filter(IPPNode.ipp_name==form_data['selectedOption'], IPPNode.node_name==form_data['node_name']).first()
        if existing_node:
            # Update existing node
            existing_node.node_name = form_data['node_name']
            existing_node.location = form_data['location']
            existing_node.distributor = form_data['distributor']
            existing_node.voltage_level = form_data['voltageLevel']
            existing_node.region = form_data['region']
            existing_node.classification = form_data['type']
            existing_node.remote_status = form_data['remote']
        else:
            # Create new node if it doesn't exist
            new_node = IPPNode(
                ipp_name=form_data['selectedOption'],
                node_name=form_data['node_name'],
                location=form_data['location'],
                distributor=form_data['distributor'],
                voltage_level=form_data['voltageLevel'],
                region=form_data['region'],
                classification=form_data['type'],
                remote_status=form_data['remote']
            )
            db.session.add(new_node)
        
        # Commit the transaction
        db.session.commit()
        return "Data stored successfully"

    elif form_data['category'] == 'Substation':
        # Check if the node already exists by 'substation' or 'node_name'
        existing_node = SubstationNode.query.filter(SubstationNode.substation==form_data['selectedOption'], SubstationNode.node_name==form_data['node_name']).first()
        if existing_node:
            # Update existing node
            existing_node.node_name = form_data['node_name']
            existing_node.location = form_data['location']
            existing_node.distributor = form_data['distributor']
            existing_node.voltage_level = form_data['voltageLevel']
            existing_node.region = form_data['region']
            existing_node.category = form_data['category']
            existing_node.remote_status = form_data['remote']
        else:
            # Create new node if it doesn't exist
            new_node = SubstationNode(
                substation=form_data['selectedOption'],
                node_name=form_data['node_name'],
                location=form_data['location'],
                distributor=form_data['distributor'],
                voltage_level=form_data['voltageLevel'],
                region=form_data['region'],
                category=form_data['category'],
                remote_status=form_data['remote']
            )
            db.session.add(new_node)
        
        # Commit the transaction
        db.session.commit()
        return "Data stored successfully"

    elif form_data['category'] == 'Standalone':
        # Check if the node already exists by 'node_name' (you can also use other fields like 'distributor1')
        existing_node = StandaloneNode.query.filter_by(node_name=form_data['node_name']).first()
        if existing_node:
            # Update existing node
            existing_node.location = form_data['location']
            existing_node.distributor1 = form_data['distributor_1']
            existing_node.distributor2 = form_data['distributor_2']
            existing_node.voltage_level = form_data['voltageLevel']
            existing_node.region = form_data['region']
            existing_node.classification = form_data['type']
            existing_node.remote_status = form_data['remote']
        else:
            # Create new node if it doesn't exist
            new_node = StandaloneNode(
                node_name=form_data['node_name'],
                location=form_data['location'],
                distributor1=form_data['distributor_1'],
                distributor2=form_data['distributor_2'],
                voltage_level=form_data['voltageLevel'],
                region=form_data['region'],
                classification=form_data['type'],
                remote_status=form_data['remote']
            )
            db.session.add(new_node)
        
        # Commit the transaction
        db.session.commit()
        return "Data stored successfully"

    
def store_energy_meter_data(form_data, db):
    # Check if a record with the same serial_no already exists
    existing_meter = energyMeters.query.filter_by(serial_no=form_data['serial_no']).first()
    
    if existing_meter:
        # If the meter already exists, update the fields with the new data
        existing_meter.meter_category = form_data['meter_category']
        existing_meter.sub_ipp_name = form_data['sub_ipp_name']
        existing_meter.node_name = form_data['nodeName']
        existing_meter.meter_classification = form_data['meter_classification']
        existing_meter.manufacturer = form_data['manufacturer']
        existing_meter.meter_type = form_data['meter_type']
        existing_meter.YOM = form_data['YOM']
        existing_meter.accuracy = form_data['accuracy']
        existing_meter.meter_usage = form_data['meter_usage']
        existing_meter.no_of_elements = form_data['no_of_elements']
        existing_meter.CT_ratio = form_data['CT_ratio']
        existing_meter.VT_ratio = form_data['VT_ratio']
        
        # Commit the changes
        db.session.commit()
        
        return "Data stored successfully"
    
    # Check if a meter with the same category, node_name, and sub_ipp_name exists eg from meter replacement
    existing_node_meter = energyMeters.query.filter_by(
        meter_category=form_data['meter_category'],
        node_name=form_data['nodeName'],
        sub_ipp_name=form_data['sub_ipp_name'],
        meter_usage = form_data['meter_usage']
    ).first()

    if existing_node_meter:
        # If the node meter exists, update its values
        existing_meter.serial_no = form_data['serial_no']
        existing_meter.meter_category = form_data['meter_category']
        existing_meter.sub_ipp_name = form_data['sub_ipp_name']
        existing_meter.node_name = form_data['nodeName']
        existing_meter.meter_classification = form_data['meter_classification']
        existing_meter.manufacturer = form_data['manufacturer']
        existing_meter.meter_type = form_data['meter_type']
        existing_meter.YOM = form_data['YOM']
        existing_meter.accuracy = form_data['accuracy']
        existing_meter.meter_usage = form_data['meter_usage']
        existing_meter.no_of_elements = form_data['no_of_elements']
        existing_meter.CT_ratio = form_data['CT_ratio']
        existing_meter.VT_ratio = form_data['VT_ratio']
        
        db.session.commit()  # Commit the updates

        return "Data stored successfully"
   
    else:
        # If the meter does not exist, create a new record
        new_energy_meter = energyMeters(
            serial_no=form_data['serial_no'],
            meter_category=form_data['meter_category'],
            sub_ipp_name = form_data['sub_ipp_name'],
            node_name=form_data['nodeName'],
            meter_classification=form_data['meter_classification'],
            manufacturer=form_data['manufacturer'],
            meter_type=form_data['meter_type'],
            YOM=form_data['YOM'],
            accuracy=form_data['accuracy'],
            meter_usage=form_data['meter_usage'],
            no_of_elements=form_data['no_of_elements'],
            CT_ratio=form_data['CT_ratio'],
            VT_ratio=form_data['VT_ratio']
        )
        
        # Add the object to the session and commit the transaction
        db.session.add(new_energy_meter)
        db.session.commit()
        
        return "Data stored successfully"


# STORE MONTHLY BILLING DATA
def store_monthly_billing_data(form_data, db):
    # Check if the record already exists in the database
    existing_record = monthlyBillingData.query.filter_by(
        serial_no=form_data['serialNo'], billing_period=form_data['billingPeriodManual']
    ).first()

    if existing_record:
        # Update existing record
        print("record exists")
        existing_record.meter_category = form_data['meterCategoryManual']
        existing_record.sub_ipp_name = form_data['subIppNameManual']
        existing_record.node_name = form_data['nodeNameManual']
        existing_record.reading_date = form_data['DateTimeOfReading'].replace('T', ' ') if 'DateTimeOfReading' in form_data else None
        existing_record.cumulative_import = form_data['CumulativeImport']
        existing_record.cumulative_export = form_data['CumulativeExport']
        existing_record.rate1 = form_data['Rate1']
        existing_record.rate2 = form_data['Rate2']
        existing_record.rate3 = form_data['Rate3']
        existing_record.rate4 = form_data['Rate4']
        existing_record.rate5 = form_data['Rate5']
        existing_record.rate6 = form_data['Rate6']
        existing_record.max_dem1 = form_data['MaxDem1']
        existing_record.max_dem1_datatime = form_data['MaxDem1DateTime'].replace('T', ' ') if 'MaxDem1DateTime' in form_data else None
        existing_record.max_dem2 = form_data['MaxDem2']
        existing_record.max_dem2_datatime = form_data['MaxDem2DateTime'].replace('T', ' ') if 'MaxDem2DateTime' in form_data else None
        existing_record.max_dem3 = form_data['MaxDem3']
        existing_record.max_dem3_datatime = form_data['MaxDem3DateTime'].replace('T', ' ') if 'MaxDem3DateTime' in form_data else None
        existing_record.reactive_import = form_data['ReactiveImport']
        existing_record.reactive_export = form_data['ReactiveExport']
        existing_record.apparent_import = form_data['ApparentImport']
        existing_record.no_of_resets = form_data['NumberOfResets']
        existing_record.date_of_last_reset = form_data['DateOfLastReset'].replace('T', ' ') if 'DateOfLastReset' in form_data else None
        existing_record.programing_count = form_data['ProgrammingCount']
        existing_record.CT_ratio = form_data['CTRatio']
        existing_record.VT_ratio = form_data['VTRatio']
        
        message = "Data stored successfully"
    else:
        # Insert new record
        new_billing_data = monthlyBillingData(
            meter_category=form_data['meterCategoryManual'],
            node_name=form_data['nodeNameManual'],
            billing_period=form_data['billingPeriodManual'],
            serial_no=form_data['serialNo'],
            reading_date=form_data['DateTimeOfReading'].replace('T', ' ') if 'DateTimeOfReading' in form_data else None,
            cumulative_import=form_data['CumulativeImport'],
            cumulative_export=form_data['CumulativeExport'],
            rate1=form_data['Rate1'],
            rate2=form_data['Rate2'],
            rate3=form_data['Rate3'],
            rate4=form_data['Rate4'],
            rate5=form_data['Rate5'],
            rate6=form_data['Rate6'],
            max_dem1=form_data['MaxDem1'],
            max_dem1_datatime=form_data['MaxDem1DateTime'].replace('T', ' ') if 'MaxDem1DateTime' in form_data else None,
            max_dem2=form_data['MaxDem2'],
            max_dem2_datatime=form_data['MaxDem2DateTime'].replace('T', ' ') if 'MaxDem2DateTime' in form_data else None,
            max_dem3=form_data['MaxDem3'],
            max_dem3_datatime=form_data['MaxDem3DateTime'].replace('T', ' ') if 'MaxDem3DateTime' in form_data else None,
            reactive_import=form_data['ReactiveImport'],
            reactive_export=form_data['ReactiveExport'],
            apparent_import=form_data['ApparentImport'],
            no_of_resets=form_data['NumberOfResets'],
            date_of_last_reset=form_data['DateOfLastReset'].replace('T', ' ') if 'DateOfLastReset' in form_data else None,
            programing_count=form_data['ProgrammingCount'],
            CT_ratio=form_data['CTRatio'],
            VT_ratio=form_data['VTRatio']
        )
        db.session.add(new_billing_data)
        message = "Data stored successfully"

    # Commit the transaction
    db.session.commit()
    return message
# STORE SUBSTATION DATA
def store_substation_data(form_data, db):
    # Check if the substation already exists using a unique identifier, for example, 'name'
    existing_substation = Substation.query.filter_by(name=form_data['name']).first()

    if existing_substation:
        # Update existing substation
        existing_substation.location = form_data['location']
        existing_substation.region = form_data['region']
        existing_substation.no_of_nodes = form_data['no_of_nodes']
        existing_substation.billing_nodes = form_data['billing_nodes']
        existing_substation.energy_loss_nodes = form_data['energy_loss_nodes']
        existing_substation.manned = form_data['manned']
        
        message = "Data stored successfully"
    else:
        # Insert new substation
        new_substation = Substation(
            name=form_data['name'],
            location=form_data['location'],
            region=form_data['region'],
            no_of_nodes=form_data['no_of_nodes'],
            billing_nodes=form_data['billing_nodes'],
            energy_loss_nodes=form_data['energy_loss_nodes'],
            manned=form_data['manned']
        )
        db.session.add(new_substation)
        message = "Data stored successfully"

    # Commit the transaction
    db.session.commit()
    return message

# STORE IPP DATA
def store_ipp_data(form_data, db):
    # Check if the substation already exists using a unique identifier, for example, 'name'
    existing_ipp = IPP.query.filter_by(name=form_data['name']).first()

    if existing_ipp:
        # Update existing substation
        existing_ipp.location = form_data['location']
        existing_ipp.region = form_data['region']
        existing_ipp.no_of_billing_nodes = form_data['no_of_nodes'] 
        existing_ipp.capacity = form_data['capacity']              
        message = "Data stored successfully"
    else:
        # Insert new substation
        new_ipp = IPP(
            name=form_data['name'],
            location=form_data['location'],
            region=form_data['region'],
            no_of_billing_nodes=form_data['no_of_nodes'],
            capacity=form_data['capacity']
        )
        db.session.add(new_ipp)
        message = "Data stored successfully"

    # Commit the transaction
    db.session.commit()
    return message

# store data using files
def store_data_from_file(file, db):
    # Read the file and store the data in the database
    pass

    
