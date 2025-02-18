// Description: This script is used to populate the meter type dropdown based on the selected manufacturer
//  and validate the form before submission.
document.getElementById('manufacturer').addEventListener('change', function() {
    var typeSelect = document.getElementById('type');
    typeSelect.innerHTML = ''; // Clear existing options

    var options = {
        'Elster': ['Select meter type','Elster A1700', 'Elster A1500'],
        'Secure Meters': ['Select meter type','CEWE Prometer', 'CEWE Prometer 100'],
        'Landis & Gyr': ['Select meter type','LG E650']
    };

    var selectedManufacturer = this.value;
    if (options[selectedManufacturer]) {
        options[selectedManufacturer].forEach(function(option) {
            var opt = document.createElement('option');
            opt.value = option;
            opt.innerHTML = option;
            typeSelect.appendChild(opt);
        });
    }
});

// Validate form before submission
document.getElementById('energyMeterForm').addEventListener('submit', function(event) {
    var selects = document.querySelectorAll('select');
    var isValid = true;

    selects.forEach(function(select) {
        if (select.value === 'default_value' || select.value === 'Select meter type') {
        select.style.borderColor = 'red';
        isValid = false;
        } else {
        select.style.borderColor = '';
        }
    });

    if (!isValid) {
        event.preventDefault();
        alert('Please select a valid option for all fields.');
    }
    });
