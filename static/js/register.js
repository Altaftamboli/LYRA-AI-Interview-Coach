document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    if (!registerForm) {
        console.error("registerForm not found");
        return;
    }

    registerForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        console.log("Register button clicked");

        const fullname = document.getElementById("fullname").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (!fullname || !email || !password || !confirmPassword) {
            alert("Please fill all fields.");
            return;
        }

        if (fullname.length < 3) {
            alert("Name must contain at least 3 characters.");
            return;
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            alert("Enter a valid email address.");
            return;
        }

        if (password.length < 6) {
            alert("Password must be at least 6 characters.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {

            console.log("Sending registration request...");

            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: fullname,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            console.log("Server response:", data);

            if (response.ok) {

                alert(data.message);

                window.location.href = "/login";

            } else {

                alert(data.message);

            }

        } catch (error) {

            console.error("Registration Error:", error);

            alert("Unable to connect to server.");

        }

    });

});