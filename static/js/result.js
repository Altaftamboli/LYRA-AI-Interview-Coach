// ===============================
// AI Interview Coach - result.js
// ===============================

// Sample Result Data
const result = {
    score: 85,
    totalQuestions: 10,
    correctAnswers: 8,
    strengths: [
        "Good HTML & CSS knowledge",
        "Strong JavaScript fundamentals",
        "Confident communication"
    ],
    weaknesses: [
        "Need to improve React.js",
        "Practice API integration",
        "Improve problem-solving speed"
    ],
    suggestions: [
        "Practice coding daily for 1 hour",
        "Build more frontend projects",
        "Revise JavaScript ES6 concepts"
    ]
};

// Display Score
const scoreElement = document.querySelector(".display-3");
if (scoreElement) {
    scoreElement.innerText = result.score + "%";
}

// Download Report Button
const downloadBtn = document.querySelector(".btn-success");

if (downloadBtn) {
    downloadBtn.addEventListener("click", function () {

        const report = `
==============================
      AI INTERVIEW REPORT
==============================

Overall Score : ${result.score}%
Total Questions : ${result.totalQuestions}
Correct Answers : ${result.correctAnswers}

Strengths:
- ${result.strengths.join("\n- ")}

Weaknesses:
- ${result.weaknesses.join("\n- ")}

Suggestions:
- ${result.suggestions.join("\n- ")}

Thank you for using AI Interview Coach.
`;

        const blob = new Blob([report], { type: "text/plain" });

        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "AI_Interview_Report.txt";
        link.click();
    });
}

// Retake Interview Button
const retakeBtn = document.querySelector(".btn-warning");

if (retakeBtn) {
    retakeBtn.addEventListener("click", function () {
        if (confirm("Do you want to retake the interview?")) {
            window.location.href = "interview.html";
        }
    });
}

// Dashboard Button
const dashboardBtn = document.querySelector(".btn-primary");

if (dashboardBtn) {
    dashboardBtn.addEventListener("click", function () {
        window.location.href = "dashboard.html";
    });
}