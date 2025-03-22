document.getElementById("button").addEventListener("click", function (event) {
    event.preventDefault();

    // clear previous errors
    document.querySelectorAll(".error-message").forEach(span => {
        span.style.display = "none";
        span.textContent = "";
    });

    let save = true;
    
    // get value + sanitize
    const email = document.getElementById("email").value.trim();
    const fullname = document.getElementById("fullname").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const rpt_password = document.getElementById("rpt_password").value;

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

    if (!rpt_password){
        const rptPasswordError = document.getElementById("rpt_passwordError");
        rptPasswordError.textContent = "Re-enter your password";
        rptPasswordError.style.display = 'block';
        save = false;
    }

    if (rpt_password !== password) {
        const passwordError = document.getElementById("rpt_passwordError");
        passwordError.textContent = "Password does not match";
        passwordError.style.display = "block";
        save = false;
    }

    // submit if passes the validation
    if (save === true){
        document.querySelector("form").submit();
    }
});
