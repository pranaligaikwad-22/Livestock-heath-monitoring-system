// Translations for Cow Disease Prediction System
const translations = {
  en: {
    // Header & Navigation
    logo: "Livestock Disease Prediction",
    navHome: "Home",
    navDetect: "Detect Disease",
    navAppointment: "Book Appointment",
    navHistory: "History",
    navExpert: "Ask Expert",
    navDoctors: "Our Doctors",
    aiBadge: "AI-Powered Veterinary Solution",
    heroTitle: "Livestock Disease Prediction Using AI & Machine Learning",
    heroDescription:
      "Upload an image of your cow and get instant disease detection results with treatment recommendations powered by advanced AI technology.",
    startDetection: "Start Detection",
    learnMore: "Learn More",
    accuracy: "Accuracy Rate",
    detectionTime: "Detection Time",
    available: "Available",

    // Upload Section
    uploadTitle: "Upload Cow Image",
    uploadText: "Drag & drop your image here or click to browse",
    fileInfo: "Supports: JPG, PNG, JPEG (Max 16MB)",
    predictBtn: "Predict Disease",
    clearBtn: "Clear Results",
    cameraBtn: "USE-CAMERA",
    galleryBtn: "USE-GALLERY",

    // Model Warning
    modelWarning: "Model Not Available",
    modelWarningText: "The AI model has not been trained yet.",
    modelWarningFix: "To fix this:",
    modelWarningCommand:
      "Run python train_model.py in your terminal to train the model first.",

    // Results
    resultsTitle: "Prediction Results",
    confidence: "Confidence",
    severity: "Severity",
    urgency: "Urgency",

    // Suggestions
    suggestionsTitle: "Doctor's Recommendations",

    // Chatbot
    chatbotTitle: "Disease Information Chatbot",
    chatbotPlaceholder: "Ask about cow diseases...",
    chatbotWelcome:
      "Hello! I'm here to help you with information about cow diseases. Ask me about symptoms, prevention, or treatment.",

    // Appointment
    appointmentTitle: "Book Doctor Appointment",
    appointmentDescription:
      "Schedule an appointment with our veterinary experts for professional consultation and treatment.",
    patientName: "Patient Name (Cow ID)",
    ownerName: "Owner Name",
    phone: "Phone Number",
    email: "Email Address",
    appointmentDate: "Preferred Date",
    appointmentTime: "Preferred Time",
    symptoms: "Symptoms / Reason for Visit",
    symptomsPlaceholder:
      "Describe the symptoms or reason for the appointment...",
    urgencyLevel: "Urgency Level",
    urgencyNormal: "Normal",
    urgencyUrgent: "Urgent",
    urgencyEmergency: "Emergency",
    location: "Location",
    locationPlaceholder: "Enter your location/address",
    bookAppointment: "Book Appointment",
    appointmentSuccessTitle: "Appointment Booked Successfully!",
    appointmentSuccessMessage:
      "Your appointment has been booked. We will contact you shortly to confirm the details.",

    // Disease Names
    healthy: "Healthy",
    lumpy: "Lumpy Skin Disease",
    footAndMouth: "Foot and Mouth Disease",

    // Severity Levels
    none: "None",
    low: "Low",
    high: "High",
    critical: "Critical",

    // Loading
    analyzing: "Analyzing image...",

    // Errors
    errorPredictionFailed: "Prediction failed",
    errorModelNotFound:
      "Model not found. Please train the model first by running 'python train_model.py'",
    errorNoFile: "No file selected",
    errorInvalidImage:
      "Please upload a valid cow image. The uploaded image does not appear to be of a cow.",

    // Doctor Suggestions
    healthyTitle: "Healthy Cow",
    healthyDesc: "Your cow appears to be healthy!",
    lumpyTitle: "Lumpy Skin Disease",
    lumpyDesc: "Your cow may be affected by Lumpy Skin Disease (LSD).",
    fmdTitle: "Foot and Mouth Disease",
    fmdDesc: "Your cow may be affected by Foot and Mouth Disease (FMD).",
  },
  hi: {
    // Header & Navigation
    logo: "पशुधन रोग भविष्यवाणी",
    navHome: "होम",
    navDetect: "रोग का पता लगाएं",
    navAppointment: "अपॉइंटमेंट बुक करें",
    navHistory: "इतिहास",
    navExpert: "विशेषज्ञ से पूछें",
    navDoctors: "हमारे डॉक्टर",
    aiBadge: "AI-संचालित पशुचिकित्सा समाधान",
    heroTitle: "AI और मशीन लर्निंग का उपयोग करके पशुधन रोग भविष्यवाणी",
    heroDescription:
      "अपनी गाय की एक छवि अपलोड करें और उन्नत AI तकनीक द्वारा संचालित उपचार सिफारिशों के साथ तत्काल रोग का पता लगाने के परिणाम प्राप्त करें।",
    startDetection: "पता लगाना शुरू करें",
    learnMore: "अधिक जानें",
    accuracy: "सटीकता दर",
    detectionTime: "पता लगाने का समय",
    available: "उपलब्ध",

    // Upload Section
    uploadTitle: "गाय की छवि अपलोड करें",
    uploadText: "अपनी छवि को यहाँ खींचें या ब्राउज़ करने के लिए क्लिक करें",
    fileInfo: "समर्थित: JPG, PNG, JPEG (अधिकतम 16MB)",
    predictBtn: "बीमारी की भविष्यवाणी करें",
    clearBtn: "परिणाम साफ़ करें",
    cameraBtn: "कैमरा-उपयोग करें",
    galleryBtn: "गैलरी-उपयोग करें",
    modelWarningCommand:
      "पहले मॉडल को प्रशिक्षित करने के लिए अपने टर्मिनल में python train_model.py चलाएं।",

    // Results
    resultsTitle: "भविष्यवाणी परिणाम",
    confidence: "आत्मविश्वास",
    severity: "गंभीरता",
    urgency: "तात्कालिकता",

    // Suggestions
    suggestionsTitle: "डॉक्टर की सिफारिशें",

    // Chatbot
    chatbotTitle: "रोग सूचना चैटबॉट",
    chatbotPlaceholder: "गाय की बीमारियों के बारे में पूछें...",
    chatbotWelcome:
      "नमस्ते! मैं गाय की बीमारियों के बारे में जानकारी में आपकी मदद के लिए यहाँ हूँ। मुझसे लक्षण, रोकथाम या उपचार के बारे में पूछें।",

    // Disease Names
    healthy: "स्वस्थ",
    lumpy: "लंपी त्वचा रोग",
    footAndMouth: "पैर और मुंह की बीमारी",

    // Severity Levels
    none: "कोई नहीं",
    low: "कम",
    high: "उच्च",
    critical: "गंभीर",

    // Loading
    analyzing: "छवि का विश्लेषण कर रहे हैं...",

    // Errors
    errorPredictionFailed: "भविष्यवाणी विफल",
    errorModelNotFound:
      "मॉडल नहीं मिला। कृपया पहले 'python train_model.py' चलाकर मॉडल को प्रशिक्षित करें",
    errorNoFile: "कोई फ़ाइल चयनित नहीं",
    errorInvalidImage:
      "कृपया एक वैध गाय की छवि अपलोड करें। अपलोड की गई छवि गाय की नहीं प्रतीत होती।",

    // Doctor Suggestions
    healthyTitle: "स्वस्थ गाय",
    healthyDesc: "आपकी गाय स्वस्थ प्रतीत होती है!",
    lumpyTitle: "लंपी त्वचा रोग",
    lumpyDesc: "आपकी गाय लंपी त्वचा रोग (LSD) से प्रभावित हो सकती है।",
    fmdTitle: "पैर और मुंह की बीमारी",
    fmdDesc: "आपकी गाय पैर और मुंह की बीमारी (FMD) से प्रभावित हो सकती है।",
  },
  mr: {
    // Header & Navigation
    logo: "पशुधन रोग अंदाज",
    navHome: "मुख्यपृष्ठ",
    navDetect: "रोग शोधा",
    navAppointment: "अपॉइंटमेंट बुक करा",
    navHistory: "इतिहास",
    navExpert: "तज्ञांना विचारा",
    navDoctors: "आमचे डॉक्टर",
    aiBadge: "AI-चालित पशुवैद्यकीय उपाय",
    heroTitle: "AI आणि मशीन लर्निंग वापरून पशुधन रोग अंदाज",
    heroDescription:
      "आपल्या गायीची प्रतिमा अपलोड करा आणि प्रगत AI तंत्रज्ञानाद्वारे चालित उपचार शिफारसींसह तत्काल रोग शोध परिणाम मिळवा.",
    startDetection: "शोध सुरू करा",
    learnMore: "अधिक जाणून घ्या",
    accuracy: "अचूकता दर",
    detectionTime: "शोध वेळ",
    available: "उपलब्ध",

    // Upload Section
    uploadTitle: "गायीची प्रतिमा अपलोड करा",
    uploadText: "आपली प्रतिमा येथे ड्रॅग करा किंवा ब्राउझ करण्यासाठी क्लिक करा",
    fileInfo: "समर्थित: JPG, PNG, JPEG (कमाल 16MB)",
    predictBtn: "रोगाचा अंदाज लावा",
    clearBtn: "परिणाम साफ करा",
    cameraBtn: "कॅमेरा-वापरा",
    galleryBtn: "गॅलरी-वापरा",

    // Model Warning
    modelWarning: "मॉडेल उपलब्ध नाही",
    modelWarningText: "AI मॉडेल अद्याप प्रशिक्षित केलेले नाही.",
    modelWarningFix: "हे निराकरण करण्यासाठी:",
    modelWarningCommand:
      "प्रथम मॉडेल प्रशिक्षित करण्यासाठी आपल्या टर्मिनलमध्ये python train_model.py चालवा.",

    // Results
    resultsTitle: "अंदाज परिणाम",
    confidence: "आत्मविश्वास",
    severity: "गंभीरता",
    urgency: "तातडी",

    // Suggestions
    suggestionsTitle: "डॉक्टरांच्या शिफारसी",

    // Chatbot
    chatbotTitle: "रोग माहिती चॅटबॉट",
    chatbotPlaceholder: "गायींच्या रोगांबद्दल विचारा...",
    chatbotWelcome:
      "नमस्कार! मी गायींच्या रोगांबद्दल माहितीत आपली मदत करण्यासाठी येथे आहे. मला लक्षणे, प्रतिबंध किंवा उपचारांबद्दल विचारा.",

    // Appointment
    appointmentTitle: "डॉक्टर अपॉइंटमेंट बुक करा",
    appointmentDescription:
      "व्यावसायिक सल्लामसलत आणि उपचारासाठी आमच्या पशुवैद्यकीय तज्ञांसोबत अपॉइंटमेंट शेड्यूल करा.",
    patientName: "रुग्णाचे नाव (गाय आयडी)",
    ownerName: "मालकाचे नाव",
    phone: "फोन नंबर",
    email: "ईमेल पत्ता",
    appointmentDate: "प्राधान्य तारीख",
    appointmentTime: "प्राधान्य वेळ",
    symptoms: "लक्षणे / भेटीचे कारण",
    symptomsPlaceholder: "लक्षणे किंवा अपॉइंटमेंटचे कारण वर्णन करा...",
    urgencyLevel: "तातडीचा स्तर",
    urgencyNormal: "सामान्य",
    urgencyUrgent: "तातडीचे",
    urgencyEmergency: "आपत्कालीन",
    location: "स्थान",
    locationPlaceholder: "आपले स्थान/पत्ता प्रविष्ट करा",
    bookAppointment: "अपॉइंटमेंट बुक करा",
    appointmentSuccessTitle: "अपॉइंटमेंट यशस्वीरित्या बुक झाली!",
    appointmentSuccessMessage:
      "आपली अपॉइंटमेंट बुक झाली आहे. आम्ही तपशीलांची पुष्टी करण्यासाठी लवकरच आपल्याशी संपर्क साधू.",

    // Disease Names
    healthy: "निरोगी",
    lumpy: "लंपी त्वचा रोग",
    footAndMouth: "पाय आणि तोंडाचा रोग",

    // Severity Levels
    none: "काहीही नाही",
    low: "कमी",
    high: "उच्च",
    critical: "गंभीर",

    // Loading
    analyzing: "प्रतिमेचे विश्लेषण करत आहे...",

    // Errors
    errorPredictionFailed: "अंदाज अयशस्वी",
    errorModelNotFound:
      "मॉडेल सापडले नाही. कृपया प्रथम 'python train_model.py' चालवून मॉडेल प्रशिक्षित करा",
    errorNoFile: "कोणतीही फाइल निवडलेली नाही",
    errorInvalidImage:
      "कृपया वैध गाय प्रतिमा अपलोड करा. अपलोड केलेली प्रतिमा गायची दिसत नाही.",

    // Doctor Suggestions
    healthyTitle: "निरोगी गाय",
    healthyDesc: "आपली गाय निरोगी दिसते!",
    lumpyTitle: "लंपी त्वचा रोग",
    lumpyDesc: "आपली गाय लंपी त्वचा रोग (LSD) ने प्रभावित होऊ शकते.",
    fmdTitle: "पाय आणि तोंडाचा रोग",
    fmdDesc: "आपली गाय पाय आणि तोंडाचा रोग (FMD) ने प्रभावित होऊ शकते.",
  },
};

// Function to get translation
function t(key, lang = "en") {
  return translations[lang]?.[key] || translations["en"][key] || key;
}
