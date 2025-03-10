
xx=[{'serial_no': '67563259', 'meter_type': 'LGE650', 'meter_category': 'Substation', 'sub_ipp_name': 'kampala north'}, {'serial_no': 'WP020204', 'meter_type': 'CEWE Prometer 100', 'meter_category': 'Standalone', 'sub_ipp_name': 'default_value'}]

var serial_no = "67563259"

xx.forEach(element => {
    if(element['serial_no'] === serial_no){
        console.log("FOUND")
    } 
});


let nodeDetails = xx.find(item => 
    item['sub_ipp_name'] === 'kampala north' && item['category'] === "Substation"
    
);
//print(nodeDetails)
console.log(nodeDetails)