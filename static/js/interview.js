document.getElementById("startBtn").addEventListener("click", async function () {

    const role = document.getElementById("role").value;
    const difficulty = document.getElementById("difficulty").value;
    const questions = document.getElementById("questions").value;

    try {

        const response = await fetch("/api/start-interview", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                role,
                difficulty,
                questions
            })

        });

        const data = await response.json();

        document.getElementById("question").innerText =
            data.questions;

    }

    catch (error) {

        console.error(error);

        alert("Failed to generate AI questions.");

    }

});