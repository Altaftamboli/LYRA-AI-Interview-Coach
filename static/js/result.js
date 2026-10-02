document.addEventListener("DOMContentLoaded", function () {

    const storedResult =
        sessionStorage.getItem("interviewResult");


    if (!storedResult) {

        alert("No interview result found.");

        window.location.href =
            "/interview";

        return;

    }


    let result;

    try {

        result =
            JSON.parse(storedResult);

    } catch (error) {

        console.error(
            "Result parsing error:",
            error
        );

        alert("Invalid interview result.");

        window.location.href =
            "/interview";

        return;

    }


    const score =
        Number(result.score) || 0;


    const totalQuestions =
        Number(result.totalQuestions) || 0;


    const correctAnswers =
        Number(result.correctAnswers) || 0;


    const scoreElement =
        document.querySelector(".display-3");


    if (scoreElement) {

        scoreElement.innerText =
            `${score}%`;

    }


    const scoreText =
        document.getElementById(
            "scoreText"
        );


    if (scoreText) {

        scoreText.innerText =
            `${score}%`;

    }


    const totalQuestionsElement =
        document.getElementById(
            "totalQuestions"
        );


    if (totalQuestionsElement) {

        totalQuestionsElement.innerText =
            totalQuestions;

    }


    const correctAnswersElement =
        document.getElementById(
            "correctAnswers"
        );


    if (correctAnswersElement) {

        correctAnswersElement.innerText =
            correctAnswers;

    }


    function displayList(
        elementId,
        items
    ) {

        const element =
            document.getElementById(
                elementId
            );


        if (!element) {
            return;
        }


        element.innerHTML = "";


        if (!Array.isArray(items)) {
            return;
        }


        items.forEach(function (item) {

            const li =
                document.createElement("li");


            li.innerText =
                item;


            element.appendChild(li);

        });

    }


    displayList(
        "strengths",
        result.strengths
    );


    displayList(
        "weaknesses",
        result.weaknesses
    );


    displayList(
        "suggestions",
        result.suggestions
    );


    const feedbackElement =
        document.getElementById(
            "feedback"
        );


    if (feedbackElement) {

        feedbackElement.innerHTML = "";


        if (Array.isArray(result.feedback)) {

            result.feedback.forEach(
                function (item, index) {

                    const li =
                        document.createElement("li");


                    li.innerText =
                        `Question ${index + 1}: ${item}`;


                    feedbackElement.appendChild(
                        li
                    );

                }
            );

        }

    }


    const downloadBtn =
        document.getElementById(
            "downloadBtn"
        );


    if (downloadBtn) {

        downloadBtn.addEventListener(
            "click",
            function () {

                const report = `
================================
       LYRA INTERVIEW REPORT
================================

Overall Score: ${score}%

Total Questions: ${totalQuestions}

Correct Answers: ${correctAnswers}


STRENGTHS
--------------------------------
${(result.strengths || [])
    .map(item => "- " + item)
    .join("\n")}


WEAKNESSES
--------------------------------
${(result.weaknesses || [])
    .map(item => "- " + item)
    .join("\n")}


AI SUGGESTIONS
--------------------------------
${(result.suggestions || [])
    .map(item => "- " + item)
    .join("\n")}


QUESTION FEEDBACK
--------------------------------
${(result.feedback || [])
    .map((item, index) =>
        `Question ${index + 1}: ${item}`
    )
    .join("\n")}

================================
       LYRA AI INTERVIEW COACH
================================
`;


                const blob =
                    new Blob(
                        [report],
                        {
                            type:
                                "text/plain"
                        }
                    );


                const url =
                    URL.createObjectURL(
                        blob
                    );


                const link =
                    document.createElement(
                        "a"
                    );


                link.href = url;

                link.download =
                    "LYRA_Interview_Report.txt";


                document.body.appendChild(
                    link
                );


                link.click();


                document.body.removeChild(
                    link
                );


                URL.revokeObjectURL(
                    url
                );

            }
        );

    }


    const retakeBtn =
        document.getElementById(
            "retakeBtn"
        );


    if (retakeBtn) {

        retakeBtn.addEventListener(
            "click",
            function () {

                sessionStorage.removeItem(
                    "interviewResult"
                );


                window.location.href =
                    "/interview";

            }
        );

    }


    const dashboardBtn =
        document.getElementById(
            "dashboardBtn"
        );


    if (dashboardBtn) {

        dashboardBtn.addEventListener(
            "click",
            function () {

                window.location.href =
                    "/dashboard";

            }
        );

    }

});