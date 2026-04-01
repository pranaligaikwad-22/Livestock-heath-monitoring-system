// DOM Elements
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const cameraInput = document.getElementById("cameraInput");
const cameraBtn = document.getElementById("cameraBtn");
const galleryBtn = document.getElementById("galleryBtn");
const cameraPreview = document.getElementById("cameraPreview");
const cameraVideo = document.getElementById("cameraVideo");
const cameraCanvas = document.getElementById("cameraCanvas");
const captureBtn = document.getElementById("captureBtn");
const cancelCameraBtn = document.getElementById("cancelCameraBtn");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");
const removeImage = document.getElementById("removeImage");
const predictBtn = document.getElementById("predictBtn");
const clearBtn = document.getElementById("clearBtn");
const resultsSection = document.getElementById("resultsSection");
const suggestionsSection = document.getElementById("suggestionsSection");
const loadingOverlay = document.getElementById("loadingOverlay");
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const languageSelectBtn = document.getElementById("languageSelectBtn");
const langDropdown = document.getElementById("langDropdown");
const langCode = document.getElementById("langCode");
const startDetectionBtn = document.getElementById("startDetectionBtn");
const learnMoreBtn = document.getElementById("learnMoreBtn");

let selectedFile = null;
let currentLanguage = localStorage.getItem("language") || "en";
let currentPrediction = null; // Store current prediction data
let cameraStream = null; // Store camera stream

// Language code mapping
const langCodes = {
  en: "EN",
  hi: "HI",
  mr: "MR",
};

// Initialize language
langCode.textContent = langCodes[currentLanguage] || "EN";
translatePage(currentLanguage);

// Language switcher dropdown
languageSelectBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  langDropdown.classList.toggle("show");
});

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  if (!languageSelectBtn.contains(e.target)) {
    langDropdown.classList.remove("show");
  }
});

// Language option selection
document.querySelectorAll(".lang-option").forEach((option) => {
  option.addEventListener("click", (e) => {
    const lang = e.target.getAttribute("data-lang");
    currentLanguage = lang;
    localStorage.setItem("language", currentLanguage);
    langCode.textContent = langCodes[lang] || "EN";
    langDropdown.classList.remove("show");
    translatePage(currentLanguage);

    // Update document direction for RTL languages if needed
    if (currentLanguage === "hi" || currentLanguage === "mr") {
      document.body.style.fontFamily =
        "'Noto Sans Devanagari', 'Poppins', sans-serif";
    } else {
      document.body.style.fontFamily = "'Poppins', sans-serif";
    }
  });
});

// Scroll to detection section
if (startDetectionBtn) {
  startDetectionBtn.addEventListener("click", () => {
    document.getElementById("detect").scrollIntoView({ behavior: "smooth" });
  });
}

// Smooth scroll for navigation links
document.querySelectorAll(".nav-link").forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const targetId = link.getAttribute("href").substring(1);
    if (
      targetId === "detect" ||
      targetId === "expert" ||
      targetId === "history" ||
      targetId === "appointment"
    ) {
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth" });
      }
    }
  });
});

// Translate page function
function translatePage(lang) {
  // Translate all elements with data-translate attribute
  document.querySelectorAll("[data-translate]").forEach((element) => {
    const key = element.getAttribute("data-translate");
    element.textContent = t(key, lang);
  });

  // Translate placeholders
  document
    .querySelectorAll("[data-translate-placeholder]")
    .forEach((element) => {
      const key = element.getAttribute("data-translate-placeholder");
      element.placeholder = t(key, lang);
    });

  // Update loading overlay
  const loadingText = loadingOverlay.querySelector("p");
  if (loadingText) {
    loadingText.textContent = t("analyzing", lang);
  }

  // Update chatbot welcome message
  const welcomeMsg = chatMessages.querySelector(".bot-message p");
  if (welcomeMsg) {
    welcomeMsg.textContent = t("chatbotWelcome", lang);
  }
}

// Disease name mapping
const diseaseNames = {
  healthy: { en: "Healthy", hi: "स्वस्थ", mr: "निरोगी" },
  lumpy: {
    en: "Lumpy Skin Disease",
    hi: "लंपी त्वचा रोग",
    mr: "लंपी त्वचा रोग",
  },
  "foot-and-mouth": {
    en: "Foot and Mouth Disease",
    hi: "पैर और मुंह की बीमारी",
    mr: "पाय आणि तोंडाचा रोग",
  },
};

function getDiseaseName(diseaseKey, lang) {
  return (
    diseaseNames[diseaseKey]?.[lang] ||
    diseaseNames[diseaseKey]?.en ||
    diseaseKey
  );
}

// Upload area click
uploadArea.addEventListener("click", () => {
  fileInput.click();
});

// File input change
fileInput.addEventListener("change", (e) => {
  handleFileSelect(e.target.files[0]);
});

// Camera button click
cameraBtn.addEventListener("click", async () => {
  try {
    // Request camera access
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }, // Use back camera on mobile
      audio: false,
    });

    // Show camera preview
    cameraVideo.srcObject = cameraStream;
    cameraPreview.style.display = "block";
    uploadArea.style.display = "none";

    // Scroll to camera
    cameraPreview.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) {
    console.error("Error accessing camera:", error);
    alert("Unable to access camera. Please check permissions and try again.");
  }
});

// Camera input change (fallback)
cameraInput.addEventListener("change", (e) => {
  handleFileSelect(e.target.files[0]);
});

// Capture button click
captureBtn.addEventListener("click", () => {
  // Set canvas size to video size
  cameraCanvas.width = cameraVideo.videoWidth;
  cameraCanvas.height = cameraVideo.videoHeight;

  // Draw current video frame to canvas
  const ctx = cameraCanvas.getContext("2d");
  ctx.drawImage(cameraVideo, 0, 0, cameraCanvas.width, cameraCanvas.height);

  // Convert canvas to blob
  cameraCanvas.toBlob(
    (blob) => {
      // Create a File object from the blob
      const capturedFile = new File(
        [blob],
        `camera_capture_${Date.now()}.jpg`,
        { type: "image/jpeg" },
      );

      // Stop camera stream
      stopCamera();

      // Process the captured image
      handleFileSelect(capturedFile);
    },
    "image/jpeg",
    0.9,
  );
});

// Cancel camera button click
cancelCameraBtn.addEventListener("click", () => {
  stopCamera();
});

// Function to stop camera
function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach((track) => track.stop());
    cameraStream = null;
  }
  cameraVideo.srcObject = null;
  cameraPreview.style.display = "none";
  uploadArea.style.display = "block";
}

// Gallery button click
galleryBtn.addEventListener("click", () => {
  fileInput.click();
});

// Drag and drop
uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadArea.style.borderColor = "#764ba2";
  uploadArea.style.background = "#f0f2ff";
});

uploadArea.addEventListener("dragleave", () => {
  uploadArea.style.borderColor = "#667eea";
  uploadArea.style.background = "#f8f9ff";
});

uploadArea.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadArea.style.borderColor = "#667eea";
  uploadArea.style.background = "#f8f9ff";

  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    handleFileSelect(file);
  }
});

// Handle file selection
function handleFileSelect(file) {
  if (!file) return;

  if (!file.type.startsWith("image/")) {
    const errorMsg = t("errorNoFile", currentLanguage);
    alert(errorMsg);
    return;
  }

  // Stop camera if it's running
  stopCamera();

  selectedFile = file;
  const reader = new FileReader();

  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewContainer.style.display = "block";
    uploadArea.style.display = "block"; // Keep upload area visible
    predictBtn.disabled = false;
  };

  reader.readAsDataURL(file);
}

// Remove image
removeImage.addEventListener("click", () => {
  selectedFile = null;
  previewContainer.style.display = "none";
  uploadArea.style.display = "block";
  predictBtn.disabled = true;
  fileInput.value = "";
  resultsSection.style.display = "none";
  suggestionsSection.style.display = "none";
  stopCamera(); // Stop camera if running
});

// Predict button
predictBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("language", currentLanguage); // Send language preference

  loadingOverlay.style.display = "flex";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      displayResults(data);
    } else {
      let errorMsg = t("errorPredictionFailed", currentLanguage);

      // Check for specific error messages
      if (data.error && data.error.includes("valid cow image")) {
        errorMsg = t("errorInvalidImage", currentLanguage);
      } else if (data.error) {
        errorMsg += ": " + data.error;
      }

      alert(errorMsg);
    }
  } catch (error) {
    const errorMsg = t("errorPredictionFailed", currentLanguage);
    alert(errorMsg + ": " + error.message);
  } finally {
    loadingOverlay.style.display = "none";
  }
});

// Clear Results Button
clearBtn.addEventListener("click", () => {
  // Hide results sections
  resultsSection.style.display = "none";
  suggestionsSection.style.display = "none";

  // Clear prediction data
  currentPrediction = null;

  // Hide clear button
  clearBtn.style.display = "none";

  // Reset predict button state
  predictBtn.disabled = !selectedFile;

  // Scroll back to detection section
  document.getElementById("detect").scrollIntoView({
    behavior: "smooth",
  });
});

// Display results
function displayResults(data) {
  // Store prediction data for appointment booking
  currentPrediction = {
    imageName: selectedFile.name,
    disease: data.prediction,
    confidence: data.confidence,
    uploadedAt: new Date().toISOString().slice(0, 19).replace("T", " "),
  };

  // Show result image
  document.getElementById("resultImage").src = data.image;

  // Show prediction with translated disease name
  const diseaseName = document.getElementById("diseaseName");
  diseaseName.textContent = getDiseaseName(data.prediction, currentLanguage);

  const confidence = document.getElementById("confidence");
  const confidenceLabel = t("confidence", currentLanguage);
  confidence.textContent = `${confidenceLabel}: ${data.confidence}%`;

  // Show severity with translations
  const severityIndicator = document.getElementById("severityIndicator");
  const severityLabel = t("severity", currentLanguage);
  const urgencyLabel = t("urgency", currentLanguage);
  const severityValue = t(
    data.suggestions.severity.toLowerCase(),
    currentLanguage,
  );
  const urgencyValue = t(
    data.suggestions.urgency.toLowerCase(),
    currentLanguage,
  );
  severityIndicator.textContent = `${severityLabel}: ${severityValue} | ${urgencyLabel}: ${urgencyValue}`;
  severityIndicator.className =
    "severity-indicator " + data.suggestions.severity.toLowerCase();

  // Show description (already translated from backend)
  document.getElementById("description").textContent =
    data.suggestions.description;

  // Show suggestions (already translated from backend)
  const suggestionsList = document.getElementById("suggestionsList");
  suggestionsList.innerHTML = "";

  data.suggestions.suggestions.forEach((suggestion) => {
    const item = document.createElement("div");
    item.className = "suggestion-item";
    item.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <p>${suggestion}</p>
        `;
    suggestionsList.appendChild(item);
  });

  // Show sections
  resultsSection.style.display = "block";
  suggestionsSection.style.display = "block";

  // Show clear button
  clearBtn.style.display = "inline-block";

  // Scroll to results
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Chatbot functionality
function addMessage(message, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;
  messageDiv.innerHTML = `
        <i class="fas ${isUser ? "fa-user" : "fa-robot"}"></i>
        <p>${message}</p>
    `;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add typing indicator
function addTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.className = "message bot-message typing-indicator";
  typingDiv.id = "typingIndicator";
  typingDiv.innerHTML = `
        <i class="fas fa-robot"></i>
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
  const typingIndicator = document.getElementById("typingIndicator");
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Send message
function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  // Disable input and send button while processing
  chatInput.disabled = true;
  sendBtn.disabled = true;
  sendBtn.style.opacity = "0.6";

  addMessage(message, true);
  chatInput.value = "";

  // Add typing indicator immediately
  addTypingIndicator();

  // Send to backend
  fetch("/chatbot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Remove typing indicator
      removeTypingIndicator();

      if (data.success) {
        // Add a small delay for natural feel
        setTimeout(() => {
          addMessage(data.response, false);
          // Re-enable input after response
          chatInput.disabled = false;
          sendBtn.disabled = false;
          sendBtn.style.opacity = "1";
          chatInput.focus();
        }, 300);
      } else {
        addMessage("Sorry, I encountered an error. Please try again.", false);
        // Re-enable input on error
        chatInput.disabled = false;
        sendBtn.disabled = false;
        sendBtn.style.opacity = "1";
      }
    })
    .catch((error) => {
      // Remove typing indicator
      removeTypingIndicator();
      addMessage("Sorry, I encountered an error. Please try again.", false);
      // Re-enable input on error
      chatInput.disabled = false;
      sendBtn.disabled = false;
      sendBtn.style.opacity = "1";
    });
}

sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// Appointment Form Handling
const appointmentForm = document.getElementById("appointmentForm");
const appointmentSuccess = document.getElementById("appointmentSuccess");

if (appointmentForm) {
  // Set minimum date to today
  const dateInput = document.getElementById("appointmentDate");
  if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.setAttribute("min", today);
  }

  appointmentForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Check if prediction data exists
    if (!currentPrediction) {
      alert(
        "Please perform disease prediction first before booking an appointment.",
      );
      document.getElementById("detect").scrollIntoView({ behavior: "smooth" });
      return;
    }

    const formData = {
      // Prediction data
      imageName: currentPrediction.imageName,
      disease: currentPrediction.disease,
      confidence: currentPrediction.confidence,
      uploadedAt: currentPrediction.uploadedAt,
      // Appointment data
      cowId: document.getElementById("patientName").value.trim(),
      ownerName: document.getElementById("ownerName").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      email: document.getElementById("email").value.trim(),
      preferredDate: document.getElementById("appointmentDate").value,
      preferredTime: document.getElementById("appointmentTime").value,
      urgency: document.getElementById("urgency").value,
      location: document.getElementById("location").value.trim(),
    };

    // Basic validation
    if (
      !formData.ownerName ||
      !formData.phone ||
      !formData.preferredDate ||
      !formData.preferredTime
    ) {
      alert(
        "Please fill in all required fields (Owner Name, Phone, Date, and Time).",
      );
      return;
    }

    // Phone validation (basic)
    const phoneRegex = /^[0-9+\-\s()]{10,}$/;
    if (!phoneRegex.test(formData.phone)) {
      alert("Please enter a valid phone number.");
      return;
    }

    // Email validation (basic)
    if (formData.email && !formData.email.includes("@")) {
      alert("Please enter a valid email address.");
      return;
    }

    try {
      const response = await fetch("/appointment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.success) {
        // Update success message with personalized response
        const successMessageEl =
          appointmentSuccess.querySelector(".success-message p");
        if (successMessageEl && data.message) {
          successMessageEl.textContent = data.message;
        }

        appointmentForm.style.display = "none";
        appointmentSuccess.style.display = "block";
        appointmentForm.reset();

        // Scroll to success message
        appointmentSuccess.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });

        // Reset form after 5 seconds (optional)
        setTimeout(() => {
          appointmentForm.style.display = "block";
          appointmentSuccess.style.display = "none";
          // Reset to default message
          if (successMessageEl) {
            successMessageEl.textContent =
              "Your appointment has been booked. We will contact you shortly to confirm the details.";
          }
        }, 5000);
      } else {
        alert("Error: " + (data.error || "Failed to book appointment"));
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  });
}

// New Detection Button Function
function startNewDetection() {
  // Scroll to the detection section
  document.getElementById("detect").scrollIntoView({
    behavior: "smooth",
  });

  // Wait a bit for scroll to complete, then trigger file input
  setTimeout(() => {
    fileInput.click();
  }, 800);
}
