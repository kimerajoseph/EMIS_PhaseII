from models import IPPNode, SubstationNode, StandaloneNode

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
    
