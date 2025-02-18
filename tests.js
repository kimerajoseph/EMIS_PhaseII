let inputValue = "123+456-789";

// Remove + and - signs
let cleanedValue = inputValue.replace(/[+-]/g, '');

console.log(cleanedValue);  // "123456789"
