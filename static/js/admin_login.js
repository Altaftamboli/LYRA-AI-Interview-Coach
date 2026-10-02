document
    .getElementById("adminLoginForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        message.textContent = "Logging in...";

        try {

            const response = await fetch("/admin/login", {
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

            if (response.ok) {

                window.location.href = data.redirect;

            } else {

                message.textContent = data.message;
            }

        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to server.";
        }
    });