var energyMeterList = []
var serialNoMeterType = []

    function toggleForm() {
        let submissionMethod = document.getElementById("submissionMethod").value;
        document.getElementById("fileFormContainer").style.display = submissionMethod === "submitFiles" ? "block" : "none";
        document.getElementById("manualFormContainer").style.display = submissionMethod === "fillOutForm" ? "block" : "none";

    }
    // Function to format number inputs
    function formatNumber(input) {
        input.value = input.value.replace(/[^0-9.]/g, "");
    }

    // Attach the function to all number inputs on page load
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener("blur", function () {
                formatNumber(this);
            });
        });
    });

// Reset all forms on page load
    document.addEventListener("DOMContentLoaded", function () {
        // Select all forms and reset them
        document.querySelectorAll("form").forEach(form => {
            form.reset();
        });
    });

// loading metering node options
var meterCategoryManual = document.getElementById('meterCategoryManual');
var availableNodesManual = document.getElementById('nodeNameManual');
var subIppNameManual = document.getElementById('subIppNameManual');

var meterCategoryFile = document.getElementById('meterCategoryFile');
var subIppNameFile = document.getElementById('subIppNameFile');
var availableNodesFile = document.getElementById('nodeNameFile');


function updateOptionsFile() {
    console.log("function called")
    var selectedCategory = meterCategoryFile.value;
    //var subIppSelect = thisElement.name
    console.log(selectedCategory)       
    $.ajax({
        url: '/get_node_options',  // Flask endpoint
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ category: selectedCategory }),  // Send category data
        dataType: 'json',
            success: function (data) {
                console.log("function data",data);
                if (data && Array.isArray(data) && data.length > 0 && selectedCategory !== "Standalone") {
                    subIppNameFile.style.display = "block";
                    subIppNameFile.innerHTML = "";
                //availableNodes.append('<option value="default_value" selected>--Select an Option--</option>'); // Default placeholder
                subIppNameFile.innerHTML = `<option value="default_value" selected>Select an option</option>`   
                data.forEach(item => {
                    var opt = document.createElement('option');
                    opt.value = item["name"].toLowerCase();
                    // convert data.name to lower case and set it as the option text                        
                    opt.innerHTML = item["name"].toLowerCase();
                    subIppNameFile.appendChild(opt);
                });
            }

            else if (data && Array.isArray(data) && data.length > 0 && selectedCategory === "Standalone"){
                subIppNameFile.style.display = "none";
                availableNodesFile.innerHTML = `<option value="default_value" selected>Select an option</option>`   
                data.forEach(item => {
                    var opt = document.createElement('option');
                    opt.value = item["name"].toLowerCase();
                    // convert data.name to lower case and set it as the option text                        
                    opt.innerHTML = item["name"].toLowerCase();
                    availableNodesFile.appendChild(opt);
                });
            }
        },
            error: function () {
                alert('Failed to fetch options');
            }
        });
    }

// populate substation and IPP nodes based on selected category for files submission
function updateNodeOptionsFile() {
        console.log("function called")
        var selectedCategory = meterCategoryFile.value;
        var selectedIppSubstation = subIppNameFile.value
    
    console.log(selectedCategory,selectedIppSubstation)
   
    $.ajax({
        url: '/get_ipp_substation_nodes',  // Flask endpoint
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ ipp_substation: selectedIppSubstation,category:selectedCategory }), 
        dataType: 'json',
            success: function (data) {
                console.log("function data",data);
                subIppNameFile.style.display = "block";
                if (data && Array.isArray(data) && data.length > 0 ) {              
                   
                //availableNodes.append('<option value="default_value" selected>--Select an Option--</option>'); // Default placeholder
                availableNodesFile.innerHTML = `<option value="default_value" selected>Select an option</option>`   
                data.forEach(item => {
                    var opt = document.createElement('option');
                    opt.value = item["name"].toLowerCase();
                    // convert data.name to lower case and set it as the option text                        
                    opt.innerHTML = item["name"].toLowerCase();
                    availableNodesFile.appendChild(opt);
                });
            }

   else{
    alert("No nodes to display. Please add nodes first")
    availableNodesFile.innerHTML = "";
   }
        },
            error: function () {
                alert('Failed to fetch options');
            }
        });
    }


// FUNCTIONS FOR MANUAL FORM

function updateOptionsManual() {
    console.log("function called")
    var selectedCategory = meterCategoryManual.value;
    //var subIppSelect = thisElement.name
    console.log(selectedCategory)       
    $.ajax({
        url: '/get_node_options',  // Flask endpoint
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ category: selectedCategory }),  // Send category data
        dataType: 'json',
            success: function (data) {
                console.log("function data",data);
                if (data && Array.isArray(data) && data.length > 0 && selectedCategory !== "Standalone") {
                    subIppNameManual.style.display = "block";
                    subIppNameManual.innerHTML = "";
                //availableNodes.append('<option value="default_value" selected>--Select an Option--</option>'); // Default placeholder
                subIppNameManual.innerHTML = `<option value="default_value" selected>Select an option</option>`   
                data.forEach(item => {
                    var opt = document.createElement('option');
                    opt.value = item["name"].toLowerCase();
                    // convert data.name to lower case and set it as the option text                        
                    opt.innerHTML = item["name"].toLowerCase();
                    subIppNameManual.appendChild(opt);
                });
            }

            else if (data && Array.isArray(data) && data.length > 0 && selectedCategory === "Standalone"){
                subIppNameManual.style.display = "none";
                availableNodesManual.innerHTML = `<option value="default_value" selected>Select an option</option>`   
                data.forEach(item => {
                    var opt = document.createElement('option');
                    opt.value = item["name"].toLowerCase();
                    // convert data.name to lower case and set it as the option text                        
                    opt.innerHTML = item["name"].toLowerCase();
                    availableNodesManual.appendChild(opt);
                });
            }
        },
            error: function () {
                alert('Failed to fetch options');
            }
        });
    }

// populate substation and IPP nodes based on selected category for files submission
function updateNodeOptionsManual() {
        console.log("function called")
        var selectedCategory = meterCategoryManual.value;
        var selectedIppSubstation = subIppNameManual.value
    
    console.log(selectedCategory,selectedIppSubstation)
   
    $.ajax({
        url: '/get_ipp_substation_nodes',  // Flask endpoint
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ ipp_substation: selectedIppSubstation,category:selectedCategory }), 
        dataType: 'json',
            success: function (data) {
                console.log("function data",data);
                subIppNameManual.style.display = "block";
                if (data && Array.isArray(data) && data.length > 0 ) {              
                   
                //availableNodes.append('<option value="default_value" selected>--Select an Option--</option>'); // Default placeholder
                availableNodesManual.innerHTML = `<option value="default_value" selected>Select an option</option>`   
                data.forEach(item => {
                    var opt = document.createElement('option');
                    opt.value = item["name"].toLowerCase();
                    // convert data.name to lower case and set it as the option text                        
                    opt.innerHTML = item["name"].toLowerCase();
                    availableNodesManual.appendChild(opt);
                });
            }

   else{
    alert("No nodes to display. Please add nodes first")
    availableNodesManual.innerHTML = "";
   }
        },
            error: function () {
                alert('Failed to fetch options');
            }
        });
    }

    function getFirstWord(filename) {
        return filename.split("_")[0]; // Extract first word before "_"
    }

// form validation for file submission
document.getElementById("fileForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission until validation is done
    let form = document.getElementById("fileForm");

    let fileInput = document.getElementById("fileInput");
    let files = fileInput.files;
    console.log(files);
    var category = document.getElementById("meterCategoryFile").value;
    var subIppName = document.getElementById("subIppNameFile").value;
    var nodeDetails = ""

    serialNoMeterType.forEach(function(item) {
        if (item.sub_ipp_name === subIppName && item.category === category) {
            console.log("Match found:", item);
            nodeDetails = item
        }
    });

    //serialNoMeterType = data
    if (nodeDetails['meter_type'] === "CEWE Prometer 100" || nodeDetails['meter_type'] === "CEWE Prometer" ) {
        if (files.length !== 2) {
            alert("You must upload exactly two files.");
            return;
        }
    else if(files.length === 2){
        let meterNo1 = getFirstWord(files[0].name);
        let meterNo2 = getFirstWord(files[1].name);
    
        if (!energyMeterList.includes(meterNo1)) {
            //console.log("Meter exists in the list!");
            alert("Meter number does exists in the list!. Please add the meter to DB first");
            return;
        }
    
        if (meterNo1 !== meterNo2) {
            alert("Files are not from the same energy meter.");
            return;
        }
    }
        
    }

    else if(nodeDetails['meter_type'] === "Elster A1700" || nodeDetails['meter_type'] === "LGE650"){
        if (files.length !== 1) {
            alert("You must upload exactly one file.");
            return;
        }
    }
     // If everything is valid, submit the form
     form.submit();
});

// form validation for manual submission
document.getElementById("manualForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Stop form submission initially
    let form = document.getElementById("manualForm");
    let selectElements = form.querySelectorAll("select");
    let dateInputs = form.querySelectorAll("input[type='date'], input[type='datetime-local']");
    
    let isValid = true; // Flag to track validation
    let errorMessage = ""; // Store all error messages

// Validate all select elements
    selectElements.forEach(selectElement => {
        if (selectElement.value === "default_value") {
            selectElement.style.border = "1px solid red";
            isValid = false;
            errorMessage = "Please select an option for all select elements.";
        } else {
            selectElement.style.border = "1px solid black"; // Reset border
        }
    });

// Validate all date inputs
    dateInputs.forEach(dateInput => {
        if (dateInput.value === "") {
            dateInput.style.border = "1px solid red";
            isValid = false;
            errorMessage = "Please fill out all required date fields.";
        } else {
            dateInput.style.border = "1px solid black"; // Reset border
        }
    });

    // check that meter number exists in DB
   //var meterNo = document.getElementById("serialNo").value.strip();
   var meterNo = document.getElementById("serialNo")
   var serialNo = meterNo.value.trim()
   console.log(serialNo)

if (!energyMeterList.includes(serialNo)) {
        //console.log("Meter exists in the list!");
        errorMessage = "Meter number does exists in the list!. Please add the meter to DB first";
        isValid = false;
    }
    // Show error alert if needed
    if (!isValid) {
        alert(errorMessage);
        return;
    }
 
    // If everything is valid, submit the form
    form.submit();
});

// fetch all meter numbers
function fetchMeterNumbers(){
    $.ajax({
        url: '/get_meter_numbers',  // Flask endpoint
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
            success: function (data) {
                console.log("function data",data[0]);   
                console.log("function data",data[1]);   
                serialNoMeterType = data[1]
        if (data && Array.isArray(data[0]) && data.length <= 0 ) { 
             alert('Failed to fetch options'); 
             }       
            else{
                energyMeterList = data[0]
                serialNoMeterType = data[1]
                console.log(energyMeterList)
        }  
    }, 
        });
    }

    document.addEventListener("DOMContentLoaded", function() {
        fetchMeterNumbers();
      });