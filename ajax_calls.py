#from flask import jsonify
from models import Substation,IPP,StandaloneNode,IPPNode,SubstationNode,energyMeters

#@app.route('/get_substations', methods=['GET'])
def get_substations():
    # Fetch all substations
    substations = Substation.query.all()
    # Convert to a list of dictionaries for easy JSON response
    substations_list = []
    for substation in substations:
        substations_list.append({
            'name': substation.name,
        })

    # Return as JSON
    return substations_list

def get_ipps():
    # Fetch all substations
    ipps = IPP.query.all()
    print("IPPS", ipps)
    # Convert to a list of dictionaries for easy JSON response
    ipps_list = []
    for ipp in ipps:
        ipps_list.append({
            'name': ipp.name,
        })
    print("LIST: ",ipps_list)
    # Return as JSON
    return ipps_list

def get_standalones():
    # Fetch all substations
    standaloneNodes = StandaloneNode.query.all()
    print("Standalones", standaloneNodes)
    # Convert to a list of dictionaries for easy JSON response
    standaloneNodes_list = []
    for node in standaloneNodes:
        standaloneNodes_list.append({
            'name': node.node_name
        })
    print("LIST: ",standaloneNodes_list)
    # Return as JSON
    return standaloneNodes_list


def get_substation_nodes(ipp_substation):
    # Fetch all substations
    substation_nodes = SubstationNode.query.filter_by(substation=ipp_substation).all()
    substation_nodes_list = []
    for node in substation_nodes:
        substation_nodes_list.append({
            'name': node.node_name
        })
    print("LIST: ",substation_nodes_list)
    # Return as JSON
    return substation_nodes_list

def get_ipp_nodes(ipp_substation):
    # Fetch all substations
    ipp_nodes = IPPNode.query.filter_by(ipp_name=ipp_substation).all()
    #print("IPPS", ipps)
    # Convert to a list of dictionaries for easy JSON response
    ipp_nodes_list = []
    for ipp_node in ipp_nodes_list:
        ipp_nodes_list.append({
            'name': ipp_node.node_name,
        })
    print("LIST: ",ipp_nodes_list)
    # Return as JSON
    return ipp_nodes_list


# get meter numbers
def get_meter_numbers(db):
    print("ajax called in backend")

    meter_number_list = []
    meter_number_and_type = []
    meters = energyMeters.query.with_entities(energyMeters.serial_no, energyMeters.meter_type,
            energyMeters.meter_category,energyMeters.sub_ipp_name,energyMeters.node_name).all()

    # Loop through the meters and create the dictionary structure
    for meter in meters:
        meter_number_and_type.append({
            "serial_no": meter.serial_no,
            "meter_type": meter.meter_type,
            "meter_category":meter.meter_category,
            "sub_ipp_name":meter.sub_ipp_name,
            "node_name": meter.node_name
        })
        meter_number_list.append(meter.serial_no)
    print(meter_number_and_type, meter_number_list)
    return meter_number_list,meter_number_and_type
