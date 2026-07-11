// ===============================
// AI Interview Coach - interview.js
// ===============================

// Sample Questions
const questions = [
    "What is HTML?",
    "What is the difference between HTML and HTML5?",
    "Explain CSS Box Model.",
    "What is Flexbox?",
    "What is JavaScript?",
    "Difference between var, let and const?",
    "What is DOM?",
    "What is Bootstrap?",
    "What is Responsive Web Design?",
    "What are API and JSON?"
];

let currentQuestion = 0;

// Elements
const questionElement = document.getElementById("question");
const answerElement = document.getElementById("answer");

// Show Question
function loadQuestion() {
    questionElement.innerText = questions[currentQuestion];
}

// Load first question
if (questionElement) {
    loadQuestion();
}

// Next Button
const nextBtn = document.querySelector(".btn-primary");

if (nextBtn) {
    nextBtn.addEventListener("click", () => {

        if (answerElement.value.trim() === "") {
            alert("Please answer the question.");
            return;
        }

        answerElement.value = "";

        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            loadQuestion();
        } else {
            alert("All questions completed.");
        }

    });
}

// Previous Button
const previousBtn = document.querySelector(".btn-secondary");

if (previousBtn) {
    previousBtn.addEventListener("click", () => {

        if (currentQuestion > 0) {
            currentQuestion--;
            loadQuestion();
        }

    });
}

// Submit Button
const submitBtn = document.querySelector(".btn-success");

if (submitBtn) {
    submitBtn.addEventListener("click", () => {

        if (confirm("Submit Interview?")) {
            window.location.href = "result.html";
        }

    });
}

// Interview Timer
const timer = document.getElementById("timer");

if (timer) {

    let minutes = 15;
    let seconds = 0;

    const countdown = setInterval(() => {

        if (seconds === 0) {

            if (minutes === 0) {
                clearInterval(countdown);
                alert("Time is over!");
                window.location.href = "result.html";
                return;
            }

            minutes--;
            seconds = 59;

        } else {
            seconds--;
        }
        document.getElementById("submitBtn").addEventListener("click", function () {
          window.location.href = "result.html";
});

        timer.innerHTML =
            String(minutes).padStart(2, "0") + ":" +
            String(seconds).padStart(2, "0");

    }, 1000);

}