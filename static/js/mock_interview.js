// ==========================================
// LYRA MOCK INTERVIEW FRONTEND
// ==========================================

let questions = [];
let currentQuestion = 0;
let answers = [];


// ==========================================
// ELEMENTS
// ==========================================

const setupSection =
    document.getElementById("setupSection");

const interviewSection =
    document.getElementById("interviewSection");

const reportSection =
    document.getElementById("reportSection");

const startMockBtn =
    document.getElementById("startMockBtn");

const nextBtn =
    document.getElementById("nextBtn");

const answerBox =
    document.getElementById("answer");

const questionText =
    document.getElementById("questionText");

const progressText =
    document.getElementById("progressText");

const progressFill =
    document.getElementById("progressFill");

const lyraMessage =
    document.getElementById("lyraMessage");

const setupLoading =
    document.getElementById("setupLoading");

const questionLoading =
    document.getElementById("questionLoading");


// ==========================================
// START MOCK INTERVIEW
// ==========================================

startMockBtn.addEventListener("click", function () {

    const role =
        document.getElementById("role").value;

    const difficulty =
        document.getElementById("difficulty").value;

    const questionCount =
        parseInt(
            document.getElementById("questionCount").value
        );


    // Demo questions for frontend testing
    questions = generateDemoQuestions(
        role,
        difficulty,
        questionCount
    );

    answers = [];

    currentQuestion = 0;


    setupSection.style.display = "none";

    interviewSection.style.display = "block";

    reportSection.style.display = "none";


    showQuestion();

});


// ==========================================
// DEMO QUESTIONS
// ==========================================

function generateDemoQuestions(
    role,
    difficulty,
    count
) {

    const demoQuestions = [

        `What are the most important skills required for a ${role}?`,

        `Explain one important concept related to ${role}.`,

        `How would you approach solving a difficult technical problem as a ${role}?`,

        `Describe a project that would demonstrate your skills as a ${role}.`,

        `How do you debug a problem in your code?`,

        `How do you keep your technical knowledge up to date?`,

        `Describe a challenging programming problem you have solved.`,

        `What is your approach to writing clean and maintainable code?`,

        `How would you optimize the performance of an application?`,

        `Why do you think you are suitable for this ${role} position?`

    ];

    return demoQuestions.slice(
        0,
        Math.min(count, demoQuestions.length)
    );
}


// ==========================================
// SHOW QUESTION
// ==========================================

function showQuestion() {

    if (
        currentQuestion >= questions.length
    ) {

        finishInterview();

        return;
    }


    const question =
        questions[currentQuestion];


    questionText.innerText =
        question;


    progressText.innerText =
        `Question ${currentQuestion + 1} of ${questions.length}`;


    const progress =
        (
            (currentQuestion + 1)
            / questions.length
        ) * 100;


    progressFill.style.width =
        `${progress}%`;


    lyraMessage.innerText =
        currentQuestion === 0

            ? "Welcome! Let's begin your mock interview. Please answer the question below."

            : "Good. Let's move to the next question.";


    // IMPORTANT:
    // Clear previous answer

    answerBox.value = "";


    answerBox.focus();


    // Hide old evaluation

    const evaluationBox =
        document.getElementById("evaluationBox");

    evaluationBox.style.display =
        "none";

}


// ==========================================
// NEXT QUESTION
// ==========================================

nextBtn.addEventListener(
    "click",
    function () {

        const answer =
            answerBox.value.trim();


        if (answer === "") {

            alert(
                "Please write your answer before continuing."
            );

            answerBox.focus();

            return;
        }


        // Save answer

        answers.push({
            question:
                questions[currentQuestion],

            answer:
                answer
        });


        currentQuestion++;


        showQuestion();

    }
);


// ==========================================
// FINISH INTERVIEW
// ==========================================

function finishInterview() {

    interviewSection.style.display =
        "none";

    reportSection.style.display =
        "block";


    generateDemoReport();

}


// ==========================================
// DEMO REPORT
// ==========================================

function generateDemoReport() {

    const score =
        calculateDemoScore();


    document.getElementById(
        "overallScore"
    ).innerText =
        `${score}%`;


    const strengthsList =
        document.getElementById(
            "strengthsList"
        );

    const weaknessesList =
        document.getElementById(
            "weaknessesList"
        );

    const suggestionsList =
        document.getElementById(
            "suggestionsList"
        );


    strengthsList.innerHTML = "";

    weaknessesList.innerHTML = "";

    suggestionsList.innerHTML = "";


    addListItem(
        strengthsList,
        "Clear communication"
    );

    addListItem(
        strengthsList,
        "Good understanding of technical concepts"
    );

    addListItem(
        strengthsList,
        "Willingness to explain your approach"
    );


    addListItem(
        weaknessesList,
        "Some answers could include more technical details"
    );

    addListItem(
        weaknessesList,
        "Improve problem-solving explanations"
    );


    addListItem(
        suggestionsList,
        "Practice technical interview questions regularly"
    );

    addListItem(
        suggestionsList,
        "Explain your reasoning step by step"
    );

    addListItem(
        suggestionsList,
        "Work on real-world projects"
    );

}


// ==========================================
// DEMO SCORE
// ==========================================

function calculateDemoScore() {

    if (answers.length === 0) {
        return 0;
    }


    let totalLength = 0;


    answers.forEach(function (item) {

        totalLength +=
            item.answer.length;

    });


    const average =
        totalLength / answers.length;


    if (average > 200) {
        return 90;
    }

    if (average > 100) {
        return 80;
    }

    if (average > 50) {
        return 70;
    }

    return 60;
}


// ==========================================
// LIST ITEM
// ==========================================

function addListItem(
    list,
    text
) {

    const li =
        document.createElement("li");

    li.innerText =
        text;

    list.appendChild(li);
}