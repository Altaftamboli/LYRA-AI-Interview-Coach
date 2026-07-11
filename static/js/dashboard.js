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
            window.location.href = "interview.html";
        });
    }

    // View Result Button
    const resultBtn = document.getElementById("viewResult");

    if (resultBtn) {
        resultBtn.addEventListener("click", () => {
            window.location.href = "result.html";
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

                window.location.href = "login.html";
                
            }
        });
    }

});