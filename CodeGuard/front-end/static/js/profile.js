// ========= TOGGLE EYE IN PW =========
document.querySelectorAll('.eye').forEach(function (eye) {
    eye.addEventListener("click", function () {
        const currentSrc = this.src.split('/').pop();
        const input = this.previousElementSibling;

        if (currentSrc.includes("icon_eyeopen.svg")) {
            this.src = "/static/assets/icon_eyeclose.svg";
            input.type = 'password';
        } else {
            this.src = "/static/assets/icon_eyeopen.svg";
            input.type = 'text';
        }
    });
});



// CHANGE SAVE CHANGES BUTTON COLOR
document.addEventListener("DOMContentLoaded", function () {
    // Select all input fields in the form
    const inputs = document.querySelectorAll(".form-profile input");

    // Select the "Save Changes" button
    const saveButton = document.querySelector(".save-btn");

    // Create a function to check if any input value has changed
    const checkForChanges = () => {
        // Iterate through all inputs to see if their current value differs from the initial value
        let hasChanges = Array.from(inputs).some((input) => {
            return input.value !== input.defaultValue; // Compare current value to the initial value
        });

        // Toggle the .not-active class based on whether changes were detected
        if (hasChanges) {
            saveButton.disabled = false;
        } else {
            saveButton.disabled = true;
        }
    };

    // Add event listeners to all input fields to detect changes
    inputs.forEach((input) => {
        input.addEventListener("input", checkForChanges); // Trigger checkForChanges on value change
    });
});




// COMPARE NEW PASSWORD AND CONFIRM PASSWORD
// DI BACKEND AJA
// const newpw = document.getElementById('new-pw');
// const confirmpw = document.getElementById('confirm-pw');

// if (newpw !== confirmpw){
// }