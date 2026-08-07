// Dashboard.js

document.addEventListener("DOMContentLoaded", () => {

    // User Name
    const userName = localStorage.getItem("username") || "User";
    const welcomeText = document.getElementById("welcomeUser");

    if (welcomeText) {
        welcomeText.textContent = `Welcome, ${userName}!`;
    }

    // Start Interview Button
    const startBtn = document.getElementById("startInterview");

    if (startBtn) {
        startBtn.addEventListener("click", () => {
            window.location.href = "/interview";
        });
    }

    // View Result Button
    const resultBtn = document.getElementById("viewResult");

    if (resultBtn) {
        resultBtn.addEventListener("click", () => {
            window.location.href = "/result";
        });
    }

    // Logout Button
    const logoutBtn = document.getElementById("logout");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {

            const confirmLogout = confirm("Are you sure you want to logout?");

            if (confirmLogout) {
                localStorage.removeItem("username");
                localStorage.removeItem("isLoggedIn");

                window.location.href = "/login";
                
            }
        });
    }

});

function startInterview() {

    const role = document.getElementById("role").value;
    const difficulty = document.getElementById("difficulty").value;
    const questions = document.getElementById("questions").value;

    localStorage.setItem("role", role);
    localStorage.setItem("difficulty", difficulty);
    localStorage.setItem("questions", questions);

    window.location.href = "/interview";
}