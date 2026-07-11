// ===============================
// AI Interview Coach - login.js
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        // Check Empty Fields
        if (email === "" || password === "") {
            alert("Please fill all fields.");
            return;
        }

        // Email Validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            alert("Please enter a valid email address.");
            return;
        }

        // Get Registered User
        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) {
            alert("No account found. Please register first.");
            window.location.href = "register.html";
            return;
        }

        // Check Credentials
        if (email === user.email && password === user.password) {

            alert("Login Successful!");

            // Save Login Status
            localStorage.setItem("isLoggedIn", "true");

            // Redirect to Dashboard
            window.location.href = "dashboard.html";
            window.location.href = "login.html";

        } else {

            alert("Invalid Email or Password!");

        }

    });

});