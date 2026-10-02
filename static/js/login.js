document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        console.error("Login form not found.");
        return;
    }

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();
            event.stopImmediatePropagation();

            const emailInput = document.getElementById("email");
            const passwordInput = document.getElementById("password");
            const loginButton = document.getElementById("loginButton");

            if (!emailInput || !passwordInput) {
                console.error("Login inputs not found.");
                return;
            }

            const email = emailInput.value.trim();
            const password = passwordInput.value;

            if (!email || !password) {

                alert("Please enter email and password.");

                return;
            }

            if (loginButton) {
                loginButton.disabled = true;
                loginButton.innerText = "Checking...";
            }

            try {

                const response = await fetch("/api/login", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "same-origin",

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                console.log(
                    "LOGIN HTTP STATUS:",
                    response.status
                );

                console.log(
                    "LOGIN RESPONSE:",
                    data
                );


                // =========================================
                // WRONG LOGIN
                // =========================================

                if (!response.ok) {

                    alert(
                        data.message ||
                        "Invalid email or password."
                    );

                    if (loginButton) {
                        loginButton.disabled = false;
                        loginButton.innerText = "Login";
                    }

                    // VERY IMPORTANT
                    // Stop here. NEVER redirect.
                    return;
                }


                // =========================================
                // SUCCESS RESPONSE WITHOUT USER
                // =========================================

                if (
                    data.success !== true ||
                    !data.user
                ) {

                    alert("Login failed.");

                    if (loginButton) {
                        loginButton.disabled = false;
                        loginButton.innerText = "Login";
                    }

                    return;
                }


                // =========================================
                // SUCCESSFUL LOGIN
                // =========================================

                console.log(
                    "AUTHENTICATED USER:",
                    data.user
                );


                if (data.user.role === "admin") {

                    window.location.replace(
                        "/admin/dashboard"
                    );

                } else {

                    window.location.replace(
                        "/dashboard"
                    );
                }

            } catch (error) {

                console.error(
                    "LOGIN ERROR:",
                    error
                );

                alert(
                    "Unable to connect to server."
                );

                if (loginButton) {
                    loginButton.disabled = false;
                    loginButton.innerText = "Login";
                }
            }

        },
        true
    );

});