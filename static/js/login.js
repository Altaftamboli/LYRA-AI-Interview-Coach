// ===============================
// AI Interview Coach - login.js
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        
        if (email === "" || password === "") {
            alert("Please fill all fields.");
            return;
        }

        
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            alert("Please enter a valid email address.");
            return;
        }

        
        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) {
            alert("No account found. Please register first.");
            window.location.href = "/register";
            return;
        }

        
        if (email === user.email && password === user.password) {



            console.log("Redirecting to dashboard...");
            localStorage.setItem("isLoggedIn", "true");
            window.location.href = "/dashboard";

            // alert("Login Successful!");

            
            // localStorage.setItem("isLoggedIn", "true");

            
            // window.location.href = "/dashboard";
            // window.location.href = "/login";

        } else {

            alert("Invalid Email or Password!");

        }

    });

});