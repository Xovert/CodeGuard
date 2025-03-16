// ========= TOGGLE SHOW PASSWORD =========
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
    const inputs = document.querySelectorAll(".form-profile input");
    const saveButton = document.querySelector(".save-btn");

    // function to check for changes
    const checkForChanges = () => {
        let hasChanges = Array.from(inputs).some((input) => {
            return input.value !== input.defaultValue;
        });

        if (hasChanges) {
            saveButton.disabled = false;
        } else {
            saveButton.disabled = true;
        }
    };

    // add event listeners to detect changes
    inputs.forEach((input) => {
        input.addEventListener("input", checkForChanges);
    });
});