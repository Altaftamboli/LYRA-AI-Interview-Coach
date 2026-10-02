// ==========================================
// LYRA AI MOCK INTERVIEW
// ==========================================

let questions = [];
let answers = [];
let evaluations = [];

let currentQuestion = 0;
let selectedRole = "";
let selectedDifficulty = "";
let questionCount = 0;

let recognition = null;
let isListening = false;


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

const evaluationBox =
    document.getElementById("evaluationBox");

const evaluationContent =
    document.getElementById("evaluationContent");

const evaluationScore =
    document.getElementById("evaluationScore");

const startSpeakingBtn =
    document.getElementById("startSpeakingBtn");

const stopSpeakingBtn =
    document.getElementById("stopSpeakingBtn");

const listeningStatus =
    document.getElementById("listeningStatus");


// ==========================================
// SPEECH RECOGNITION
// ==========================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    recognition =
        new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";


    recognition.onstart = function () {

        isListening = true;

        startSpeakingBtn.disabled = true;
        stopSpeakingBtn.disabled = false;

        listeningStatus.innerText =
            "🔴 Listening... Speak your answer.";

        listeningStatus.classList.add(
            "lyra-mock-listening"
        );
    };


    recognition.onresult = function (event) {

        let finalTranscript = "";

        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            if (
                event.results[i].isFinal
            ) {

                finalTranscript +=
                    event.results[i][0].transcript;
            }
        }


        if (
            finalTranscript.trim()
        ) {

            const existing =
                answerBox.value.trim();


            answerBox.value =
                existing
                    ? existing +
                      " " +
                      finalTranscript.trim()
                    : finalTranscript.trim();
        }
    };


    recognition.onerror = function (event) {

        console.error(
            "Speech Recognition Error:",
            event.error
        );


        isListening = false;

        startSpeakingBtn.disabled = false;
        stopSpeakingBtn.disabled = true;

        listeningStatus.innerText =
            "⚠️ Microphone error: " +
            event.error;

        listeningStatus.classList.remove(
            "lyra-mock-listening"
        );
    };


    recognition.onend = function () {

        isListening = false;

        startSpeakingBtn.disabled = false;
        stopSpeakingBtn.disabled = true;

        listeningStatus.classList.remove(
            "lyra-mock-listening"
        );


        if (
            listeningStatus.innerText.includes(
                "Listening"
            )
        ) {

            listeningStatus.innerText =
                "🎙 Microphone is off";
        }
    };

} else {

    startSpeakingBtn.disabled = true;

    listeningStatus.innerText =
        "Speech recognition is not supported in this browser.";

}


// ==========================================
// START SPEAKING
// ==========================================

startSpeakingBtn.addEventListener(
    "click",
    function () {

        if (!recognition) {

            alert(
                "Speech recognition is not supported. Please use Google Chrome or Microsoft Edge."
            );

            return;
        }


        try {

            recognition.start();

        } catch (error) {

            console.log(
                "Speech recognition is already running."
            );
        }

    }
);


// ==========================================
// STOP SPEAKING
// ==========================================

stopSpeakingBtn.addEventListener(
    "click",
    function () {

        if (
            recognition &&
            isListening
        ) {

            recognition.stop();
        }

    }
);


// ==========================================
// START MOCK INTERVIEW
// ==========================================

startMockBtn.addEventListener(
    "click",
    async function () {

        selectedRole =
            document.getElementById(
                "role"
            ).value;


        selectedDifficulty =
            document.getElementById(
                "difficulty"
            ).value;


        questionCount =
            parseInt(
                document.getElementById(
                    "questionCount"
                ).value
            );


        startMockBtn.disabled = true;

        setupLoading.style.display =
            "block";


        try {

            const response =
                await fetch(
                    "/api/mock-interview/start",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        credentials:
                            "same-origin",

                        body:
                            JSON.stringify({

                                role:
                                    selectedRole,

                                difficulty:
                                    selectedDifficulty,

                                questions:
                                    questionCount

                            })
                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.message ||
                    "Unable to start interview."
                );
            }


            questions =
                data.questions || [];


            if (
                questions.length === 0
            ) {

                throw new Error(
                    "AI did not generate questions."
                );
            }


            answers = [];
            evaluations = [];
            currentQuestion = 0;


            setupSection.style.display =
                "none";

            interviewSection.style.display =
                "block";

            reportSection.style.display =
                "none";


            showQuestion();

        } catch (error) {

            console.error(
                "Start Interview Error:",
                error
            );

            alert(
                error.message ||
                "Failed to start interview."
            );

            startMockBtn.disabled =
                false;

        } finally {

            setupLoading.style.display =
                "none";
        }

    }
);


// ==========================================
// SHOW QUESTION
// ==========================================

function showQuestion() {

    if (
        currentQuestion >=
        questions.length
    ) {

        finishInterview();

        return;
    }


    questionText.innerText =
        questions[currentQuestion];


    progressText.innerText =
        `Question ${
            currentQuestion + 1
        } of ${
            questions.length
        }`;


    const progress =
        (
            (currentQuestion + 1) /
            questions.length
        ) * 100;


    progressFill.style.width =
        `${progress}%`;


    if (
        currentQuestion === 0
    ) {

        lyraMessage.innerText =
            "Welcome! Let's begin your mock interview. Answer using your microphone or type your response.";

    } else {

        lyraMessage.innerText =
            "Good. Let's continue with the next question.";
    }


    answerBox.value = "";

    answerBox.disabled = false;


    evaluationBox.style.display =
        "none";


    evaluationContent.innerHTML =
        "";


    nextBtn.disabled = false;


    if (
        currentQuestion ===
        questions.length - 1
    ) {

        nextBtn.innerText =
            "Finish Interview →";

    } else {

        nextBtn.innerText =
            "Next Question →";
    }


    listeningStatus.innerText =
        "🎙 Microphone is off";
}


// ==========================================
// NEXT QUESTION
// ==========================================

nextBtn.addEventListener(
    "click",
    async function () {

        const answer =
            answerBox.value.trim();


        if (!answer) {

            alert(
                "Please answer the question before continuing."
            );

            answerBox.focus();

            return;
        }


        if (
            recognition &&
            isListening
        ) {

            recognition.stop();
        }


        nextBtn.disabled = true;

        answerBox.disabled = true;

        questionLoading.style.display =
            "block";


        try {

            answers[currentQuestion] = {

                question:
                    questions[currentQuestion],

                answer:
                    answer

            };


            const response =
                await fetch(
                    "/api/mock-interview/evaluate-answer",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        credentials:
                            "same-origin",

                        body:
                            JSON.stringify({

                                role:
                                    selectedRole,

                                difficulty:
                                    selectedDifficulty,

                                question:
                                    questions[currentQuestion],

                                answer:
                                    answer

                            })
                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.message ||
                    "AI evaluation failed."
                );
            }


            evaluations[currentQuestion] =
                data.evaluation;


            showEvaluation(
                data.evaluation
            );


            await delay(1800);


            currentQuestion++;


            if (
                currentQuestion >=
                questions.length
            ) {

                await finishInterview();

                return;
            }


            showQuestion();

        } catch (error) {

            console.error(
                "Evaluation Error:",
                error
            );

            alert(
                error.message ||
                "Unable to analyze your answer."
            );

            nextBtn.disabled =
                false;

            answerBox.disabled =
                false;

        } finally {

            questionLoading.style.display =
                "none";
        }

    }
);


// ==========================================
// SHOW EVALUATION
// ==========================================

function showEvaluation(
    evaluation
) {

    evaluationBox.style.display =
        "block";


    const score =
        Number(
            evaluation.score || 0
        );


    evaluationScore.innerText =
        `${score}%`;


    evaluationContent.innerHTML = `

        <div class="lyra-mock-metrics">

            <div class="lyra-mock-metric">
                <small>Technical</small>
                <strong>
                    ${
                        evaluation
                            .technical_correctness || 0
                    }%
                </strong>
            </div>


            <div class="lyra-mock-metric">
                <small>Relevance</small>
                <strong>
                    ${
                        evaluation
                            .relevance || 0
                    }%
                </strong>
            </div>


            <div class="lyra-mock-metric">
                <small>Completeness</small>
                <strong>
                    ${
                        evaluation
                            .completeness || 0
                    }%
                </strong>
            </div>


            <div class="lyra-mock-metric">
                <small>Clarity</small>
                <strong>
                    ${
                        evaluation
                            .clarity || 0
                    }%
                </strong>
            </div>

        </div>


        <div class="lyra-mock-feedback">

            <strong>
                💬 AI Feedback
            </strong>

            <p>
                ${
                    escapeHtml(
                        evaluation.feedback || ""
                    )
                }
            </p>

        </div>


        <div class="lyra-mock-feedback">

            <strong>
                💡 How to Improve
            </strong>

            <p>
                ${
                    escapeHtml(
                        evaluation.improvement || ""
                    )
                }
            </p>

        </div>
    `;
}


// ==========================================
// FINISH INTERVIEW
// ==========================================

async function finishInterview() {

    if (
        recognition &&
        isListening
    ) {

        recognition.stop();
    }


    interviewSection.style.display =
        "none";

    reportSection.style.display =
        "block";


    try {

        const response =
            await fetch(
                "/api/mock-interview/final-report",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    credentials:
                        "same-origin",

                    body:
                        JSON.stringify({

                            role:
                                selectedRole,

                            difficulty:
                                selectedDifficulty,

                            questions:
                                questions,

                            answers:
                                answers,

                            evaluations:
                                evaluations

                        })
                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                "Unable to generate report."
            );
        }


        displayFinalReport(
            data.report
        );

    } catch (error) {

        console.error(
            "Final Report Error:",
            error
        );

        alert(
            error.message ||
            "Failed to generate final report."
        );
    }
}


// ==========================================
// FINAL REPORT
// ==========================================

function displayFinalReport(
    report
) {

    document.getElementById(
        "overallScore"
    ).innerText =
        `${report.score || 0}%`;


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


    (report.strengths || [])
        .forEach(
            function (item) {

                addListItem(
                    strengthsList,
                    item
                );

            }
        );


    (report.weaknesses || [])
        .forEach(
            function (item) {

                addListItem(
                    weaknessesList,
                    item
                );

            }
        );


    (report.suggestions || [])
        .forEach(
            function (item) {

                addListItem(
                    suggestionsList,
                    item
                );

            }
        );
}


// ==========================================
// HELPERS
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


function escapeHtml(
    text
) {

    const div =
        document.createElement("div");

    div.innerText =
        text || "";

    return div.innerHTML;
}


function delay(
    milliseconds
) {

    return new Promise(
        function (resolve) {

            setTimeout(
                resolve,
                milliseconds
            );

        }
    );
}