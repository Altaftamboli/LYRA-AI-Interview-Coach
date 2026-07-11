// ===============================
// AI Interview Coach - register.js
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    registerForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const fullname = document.getElementById("fullname").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        // Check Empty Fields
        if (fullname === "" || email === "" || password === "" || confirmPassword === "") {
            alert("Please fill all fields.");
            return;
        }

        // Name Validation
        if (fullname.length < 3) {
            alert("Name must contain at least 3 characters.");
            return;
        }

        // Email Validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            alert("Enter a valid email address.");
            return;
        }

        // Password Length
        if (password.length < 6) {
            alert("Password must be at least 6 characters.");
            return;
        }

        // Password Match
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        // Save User (Temporary)
        const user = {
            fullname: fullname,
            email: email,
            password: password
        };

        localStorage.setItem("user", JSON.stringify(user));

        alert("Registration Successful!");

        // Redirect to Login Page
        window.location.href = "login.html";

    });

});