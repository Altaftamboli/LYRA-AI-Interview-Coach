let cameraStream = null;
let recognition = null;
let isListening = false;

const startLiveBtn = document.getElementById("startLiveBtn");
const setupSection = document.getElementById("setupSection");
const interviewSection = document.getElementById("interviewSection");

const camera = document.getElementById("camera");
const cameraStatus = document.getElementById("cameraStatus");
const faceStatus = document.getElementById("faceStatus");
const cameraWarning = document.getElementById("cameraWarning");

const answer = document.getElementById("answer");
const startSpeakingBtn = document.getElementById("startSpeakingBtn");
const stopSpeakingBtn = document.getElementById("stopSpeakingBtn");
const listeningStatus = document.getElementById("listeningStatus");

const voiceStatus = document.getElementById("voiceStatus");
const questionText = document.getElementById("questionText");


async function startCamera() {

    try {

        cameraStatus.innerText = "Requesting permission...";

        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });

        camera.srcObject = cameraStream;

        cameraStatus.innerText = "Camera Active";
        cameraStatus.style.color = "#20a464";

        faceStatus.innerText = "Camera is ready.";

        return true;

    } catch (error) {

        console.error("Camera Error:", error);

        cameraStatus.innerText = "Camera unavailable";
        cameraStatus.style.color = "#e5484d";

        alert(
            "Camera and microphone permission is required for Live Interview."
        );

        return false;
    }
}


function setupSpeechRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        listeningStatus.innerText =
            "Speech recognition is not supported in this browser.";

        startSpeakingBtn.disabled = true;

        return;
    }

    recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";


    recognition.onstart = function () {

        isListening = true;

        startSpeakingBtn.disabled = true;
        stopSpeakingBtn.disabled = false;

        listeningStatus.innerText =
            "🎤 Listening... Speak your answer.";

    };


    recognition.onresult = function (event) {

        let finalTranscript = "";
        let interimTranscript = "";

        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            const transcript =
                event.results[i][0].transcript;

            if (event.results[i].isFinal) {

                finalTranscript += transcript + " ";

            } else {

                interimTranscript += transcript;

            }
        }

        if (finalTranscript) {

            answer.value += finalTranscript;

        }

        if (interimTranscript) {

            listeningStatus.innerText =
                "🎤 " + interimTranscript;

        }

    };


    recognition.onerror = function (event) {

        console.error(
            "Speech Recognition Error:",
            event.error
        );

        listeningStatus.innerText =
            "Speech recognition error: " + event.error;

    };


    recognition.onend = function () {

        isListening = false;

        startSpeakingBtn.disabled = false;
        stopSpeakingBtn.disabled = true;

        listeningStatus.innerText =
            "Microphone ready.";

    };
}


function speakQuestion(text) {

    if (!window.speechSynthesis) {

        voiceStatus.innerText =
            "🔊 Voice synthesis is not supported.";

        return;

    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 0.95;
    speech.pitch = 1;
    speech.volume = 1;


    speech.onstart = function () {

        voiceStatus.innerText =
            "🔊 LYRA is asking the question...";

    };


    speech.onend = function () {

        voiceStatus.innerText =
            "🎤 Your turn. Start speaking.";

    };


    window.speechSynthesis.speak(speech);
}


startSpeakingBtn.addEventListener(
    "click",
    function () {

        if (!recognition) {

            setupSpeechRecognition();

        }

        if (!recognition || isListening) {
            return;
        }

        answer.focus();

        recognition.start();

    }
);


stopSpeakingBtn.addEventListener(
    "click",
    function () {

        if (recognition && isListening) {

            recognition.stop();

        }

    }
);


startLiveBtn.addEventListener(
    "click",
    async function () {

        startLiveBtn.disabled = true;
        startLiveBtn.innerText =
            "Starting Live Interview...";

        const cameraReady = await startCamera();

        if (!cameraReady) {

            startLiveBtn.disabled = false;
            startLiveBtn.innerText =
                "🎥 Start Live Interview";

            return;

        }

        setupSpeechRecognition();

        setupSection.style.display = "none";
        interviewSection.style.display = "block";


        questionText.innerText =
            "Hello! I am LYRA. Your live interview is ready.";

        voiceStatus.innerText =
            "🔊 LYRA is ready.";


        setTimeout(() => {

            speakQuestion(
                "Hello. Welcome to your live interview with LYRA. Please introduce yourself."
            );

        }, 500);

    }
);