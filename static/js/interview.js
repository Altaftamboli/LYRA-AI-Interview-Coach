let interviewQuestions = [];
let interviewAnswers = [];
let currentQuestionIndex = 0;

let selectedRole = "";
let selectedDifficulty = "";

let timerInterval = null;
let remainingSeconds = 15 * 60;

const startBtn = document.getElementById("startBtn");
const nextBtn = document.getElementById("nextBtn");
const questionElement = document.getElementById("question");
const answerElement = document.getElementById("answer");
const questionNumberElement = document.getElementById("questionNumber");
const timerElement = document.getElementById("timer");


function startTimer() {

    clearInterval(timerInterval);

    remainingSeconds = 15 * 60;

    updateTimer();

    timerInterval = setInterval(() => {

        remainingSeconds--;

        updateTimer();

        if (remainingSeconds <= 0) {

            clearInterval(timerInterval);

            finishInterview();

        }

    }, 1000);
}


function updateTimer() {

    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;

    if (timerElement) {

        timerElement.innerText =
            `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

    }
}


function showQuestion() {

    questionElement.innerText =
        interviewQuestions[currentQuestionIndex];

    questionNumberElement.innerText =
        `Question ${currentQuestionIndex + 1} of ${interviewQuestions.length}`;

    answerElement.value = "";
    answerElement.disabled = false;

    if (currentQuestionIndex === interviewQuestions.length - 1) {

        nextBtn.innerText = "Finish Interview";

    } else {

        nextBtn.innerText = "Next Question";

    }
}


startBtn.addEventListener("click", async function () {

    selectedRole =
        document.getElementById("role").value;

    selectedDifficulty =
        document.getElementById("difficulty").value;

    const questionCount =
        document.getElementById("questions").value;

    startBtn.disabled = true;
    startBtn.innerText = "Generating Questions...";

    try {

        const response = await fetch("/api/start-interview", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                role: selectedRole,
                difficulty: selectedDifficulty,
                questions: questionCount
            })

        });


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message || "Failed to generate questions."
            );

        }


        if (!Array.isArray(data.questions) || data.questions.length === 0) {

            throw new Error("No questions were generated.");

        }


        interviewQuestions =
            data.questions;

        interviewAnswers =
            new Array(interviewQuestions.length).fill("");

        currentQuestionIndex = 0;


        startBtn.style.display = "none";

        nextBtn.style.display = "block";

        answerElement.disabled = false;


        showQuestion();

        startTimer();


    } catch (error) {

        console.error("Start Interview Error:", error);

        alert(
            error.message ||
            "Failed to generate AI questions."
        );

        startBtn.disabled = false;

        startBtn.innerText =
            "Start Interview";

    }

});


nextBtn.addEventListener("click", async function () {

    const answer =
        answerElement.value.trim();


    if (!answer) {

        alert(
            "Please enter your answer before continuing."
        );

        return;

    }


    interviewAnswers[currentQuestionIndex] =
        answer;


    if (
        currentQuestionIndex <
        interviewQuestions.length - 1
    ) {

        currentQuestionIndex++;

        showQuestion();

        return;

    }


    await finishInterview();

});


async function finishInterview() {

    clearInterval(timerInterval);

    nextBtn.disabled = true;

    nextBtn.innerText =
        "Evaluating...";

    answerElement.disabled = true;


    try {

        const response =
            await fetch(
                "/api/evaluate-interview",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        role: selectedRole,
                        difficulty: selectedDifficulty,
                        questions: interviewQuestions,
                        answers: interviewAnswers
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Interview evaluation failed."
            );

        }


        sessionStorage.setItem(
            "interviewResult",
            JSON.stringify(data)
        );


        window.location.href =
            "/result";


    } catch (error) {

        console.error(
            "Evaluation Error:",
            error
        );


        alert(
            error.message ||
            "Failed to evaluate interview."
        );


        nextBtn.disabled = false;

        nextBtn.innerText =
            "Finish Interview";

        answerElement.disabled = false;

    }

}