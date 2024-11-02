document.getElementById("button").addEventListener("click", function (event) {
    event.preventDefault();

    // clear previous errors
    document.querySelectorAll(".error-message").forEach(span => {
        span.style.display = "none";
        span.textContent = ""; // Clear any previous messages
    });

    // ==== FUNCTIONS ====
    // sanitation function
    // function encodeHTML(input) {
    //     return input
    //         .replace(/&/g, "&amp;")
    //         .replace(/</g, "&lt;")
    //         .replace(/>/g, "&gt;")
    //         .replace(/"/g, "&quot;")
    //         .replace(/'/g, "&#39;")
    //         .replace(/:/g, "&#58;")
    //         .replace(/\(/g, "&#40;")
    //         .replace(/\)/g, "&#41;");
    // }

    let save = true;
    
    // get value + sanitize
    const email = document.getElementById("email").value.trim();
    const fullname = document.getElementById("fullname").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    // regex
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const namePattern = /^[a-zA-Z ]+$/;
    const usernamePattern = /^[a-zA-Z0-9._-]{3,20}$/;
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,40}$/;

    // ==== VALIDATIONS ====
    // email
    if (!emailPattern.test(email)) {
        const emailError = document.getElementById("emailError");
        emailError.textContent = "Please enter a valid email";
        emailError.style.display = "block";
        save = false;
    }

    // fullname
    if (!namePattern.test(fullname)) {
        const fullnameError = document.getElementById("fullnameError");
        fullnameError.textContent = "Full name can only contain letters and spaces";
        fullnameError.style.display = "block";
        save = false;
    }

    // username
    if (!usernamePattern.test(username)) {
        const usernameError = document.getElementById("usernameError");
        usernameError.textContent = "Username can only contain letters, numbers, dots, underscores, or hyphens (3-20 characters)";
        usernameError.style.display = "block";
        save = false;
    }

    // password
    if (!passwordPattern.test(password)) {
        const passwordError = document.getElementById("passwordError");
        passwordError.textContent = "Password must contain at least one uppercase, one lowercase, and one number (8-40 characters)";
        passwordError.style.display = "block";
        save = false;
    }

    // submit if passes the validation
    if (save === true){
        document.querySelector("form").submit();
    }
});
