document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        console.error("loginForm not found");
        return;
    }

    loginForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            alert("Please enter email and password.");
            return;
        }

        try {

            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.message || "Invalid Email or Password!");
                return;
            }

            console.log("Login Successful:", data);

            if (data.user.role === "admin") {
                window.location.href = "/admin/dashboard";
            } else {
                window.location.href = "/dashboard";
            }

        } catch (error) {

            console.error("Login Error:", error);
            alert("Unable to connect to server.");

        }

    });

});