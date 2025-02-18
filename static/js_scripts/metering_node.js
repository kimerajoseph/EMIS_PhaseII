    


// Initialize the form
document.addEventListener('DOMContentLoaded', function() {
    updateSubstationOptions();
});

// make border for select item black on value change
document.querySelectorAll("select").forEach(select => {
    select.addEventListener("change", function() {
        this.style.borderColor = "black";
    });
});



// Validate form before submission
document.getElementById('meteringNodeForm').addEventListener('submit', function(event) {
    var selects = document.querySelectorAll('select');
    //selects.style.borderColor = '';
    var isValid = true;
    var categoryValue = document.getElementById('category').value

    selects.forEach(function(select) {
        if (select.value === 'default_value' || select.value === 'substation_default_value' && categoryValue === 'Substation') {
        //select.style.borderColor = 'red';
        select.style.border = '2px solid red'
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

