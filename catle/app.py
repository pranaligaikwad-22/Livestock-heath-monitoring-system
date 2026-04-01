from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import numpy as np
import os
import json
from PIL import Image
import io
import base64
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cow_disease_db']
    predictions_collection = db['predictions']
    appointments_collection = db['appointments']
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    client = None

# Load model and class names
model = None
model_error = None

# Get the base directory (where app.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path1 = os.path.join(BASE_DIR, 'cow_disease_model.h5')
model_path2 = os.path.join(BASE_DIR, 'cow_disease_model_final.h5')

def load_model_lazy():
    """Lazy load the model to avoid slow TensorFlow import at startup"""
    global model, model_error
    if model is not None:
        return model

    try:
        # Import TensorFlow here to avoid slow startup
        import tensorflow as tf
        from tensorflow.keras.models import load_model

        if os.path.exists(model_path1):
            model = load_model(model_path1)
            print(f"Model loaded successfully from {model_path1}!")
        elif os.path.exists(model_path2):
            model = load_model(model_path2)
            print(f"Model loaded successfully from {model_path2}!")
        else:
            raise FileNotFoundError("No model file found")
    except Exception as e1:
        try:
            # Try relative paths as fallback
            if os.path.exists('cow_disease_model.h5'):
                model = load_model('cow_disease_model.h5')
                print("Model loaded successfully from cow_disease_model.h5 (relative path)!")
            elif os.path.exists('cow_disease_model_final.h5'):
                model = load_model('cow_disease_model_final.h5')
                print("Model loaded successfully from cow_disease_model_final.h5 (relative path)!")
            else:
                raise FileNotFoundError("No model file found in current directory")
        except Exception as e2:
            print(f"Warning: Model file not found.")
            print(f"  Attempted: {model_path1} - Error: {str(e1)}")
            print(f"  Attempted: {model_path2} - Error: {str(e2)}")
            print(f"  Current directory: {os.getcwd()}")
            print(f"  Base directory: {BASE_DIR}")
            print("Please train the model first by running: python train_model.py")
            model_error = "Model not found. Please train the model first."
            model = None
    return model

# Try to load model at startup (but don't fail if TensorFlow is slow)
try:
    load_model_lazy()
except KeyboardInterrupt:
    print("Model loading interrupted. Model will be loaded on first prediction request.")
    model = None
    model_error = "Model loading was interrupted. It will be loaded on first use."

try:
    class_json_path = os.path.join(BASE_DIR, 'class_names.json')
    if not os.path.exists(class_json_path):
        class_json_path = 'class_names.json'  # Try relative path
    
    with open(class_json_path, 'r') as f:
        class_data = json.load(f)
        # Handle both old format (list) and new format (dict)
        if isinstance(class_data, list):
            class_names = class_data
            index_to_class = None
        else:
            class_names = class_data.get('class_names', ['healthy', 'lumpy', 'foot-and-mouth'])
            class_indices = class_data.get('class_indices', {})
            index_to_class = class_data.get('index_to_class', None)
            # Convert string keys to int if needed
            if index_to_class:
                index_to_class = {int(k): v for k, v in index_to_class.items()}
    print(f"Class names loaded: {class_names}")
    if index_to_class:
        print(f"Index to class mapping: {index_to_class}")
except Exception as e:
    class_names = ['healthy', 'lumpy', 'foot-and-mouth']
    index_to_class = None
    print(f"Using default class names. Error loading class_names.json: {str(e)}")

# Doctor suggestions dictionary with multilingual support
DOCTOR_SUGGESTIONS = {
    'healthy': {
        'title': {
            'en': 'Healthy Cow',
            'hi': 'स्वस्थ गाय',
            'mr': 'निरोगी गाय'
        },
        'description': {
            'en': 'Your cow appears to be healthy!',
            'hi': 'आपकी गाय स्वस्थ प्रतीत होती है!',
            'mr': 'आपली गाय निरोगी दिसते!'
        },
        'suggestions': {
            'en': [
                'Continue regular health monitoring',
                'Maintain proper nutrition and hydration',
                'Ensure clean living conditions',
                'Schedule regular veterinary check-ups',
                'Monitor for any changes in behavior or appearance'
            ],
            'hi': [
                'नियमित स्वास्थ्य निगरानी जारी रखें',
                'उचित पोषण और जलयोजन बनाए रखें',
                'स्वच्छ रहने की स्थिति सुनिश्चित करें',
                'नियमित पशुचिकित्सा जांच शेड्यूल करें',
                'व्यवहार या उपस्थिति में किसी भी बदलाव की निगरानी करें'
            ],
            'mr': [
                'नियमित आरोग्य निरीक्षण सुरू ठेवा',
                'योग्य पोषण आणि जलयोजन राखा',
                'स्वच्छ राहणीमान सुनिश्चित करा',
                'नियमित पशुवैद्यकीय तपासणी शेड्यूल करा',
                'वर्तन किंवा देखाव्यात कोणत्याही बदलाचे निरीक्षण करा'
            ]
        },
        'severity': 'None',
        'urgency': 'Low'
    },
    'lumpy': {
        'title': {
            'en': 'Lumpy Skin Disease',
            'hi': 'लंपी त्वचा रोग',
            'mr': 'लंपी त्वचा रोग'
        },
        'description': {
            'en': 'Your cow may be affected by Lumpy Skin Disease (LSD).',
            'hi': 'आपकी गाय लंपी त्वचा रोग (LSD) से प्रभावित हो सकती है।',
            'mr': 'आपली गाय लंपी त्वचा रोग (LSD) ने प्रभावित होऊ शकते.'
        },
        'suggestions': {
            'en': [
                'Isolate the affected animal immediately to prevent spread',
                'Contact a veterinarian as soon as possible',
                'Provide supportive care: clean water, nutritious feed',
                'Monitor for fever, loss of appetite, and skin nodules',
                'Implement strict biosecurity measures',
                'Consider vaccination for other animals in the herd',
                'Disinfect equipment and facilities regularly',
                'Report to local veterinary authorities if required'
            ],
            'hi': [
                'प्रसार को रोकने के लिए प्रभावित जानवर को तुरंत अलग करें',
                'जल्द से जल्द एक पशुचिकित्सक से संपर्क करें',
                'सहायक देखभाल प्रदान करें: स्वच्छ पानी, पौष्टिक चारा',
                'बुखार, भूख न लगना और त्वचा के गांठ की निगरानी करें',
                'सख्त जैव सुरक्षा उपाय लागू करें',
                'झुंड के अन्य जानवरों के लिए टीकाकरण पर विचार करें',
                'उपकरण और सुविधाओं को नियमित रूप से कीटाणुरहित करें',
                'यदि आवश्यक हो तो स्थानीय पशुचिकित्सा अधिकारियों को रिपोर्ट करें'
            ],
            'mr': [
                'प्रसार रोखण्यासाठी प्रभावित प्राण्याला ताबडतोब वेगळे करा',
                'शक्य तितक्या लवकर पशुवैद्याशी संपर्क साधा',
                'आधारक काळजी प्रदान करा: स्वच्छ पाणी, पौष्टिक खाद्य',
                'ताप, भूक न लागणे आणि त्वचेच्या गाठींचे निरीक्षण करा',
                'कठोर जैव सुरक्षा उपाय अंमलात आणा',
                'गुरेढोरातील इतर प्राण्यांसाठी लसीकरणाचा विचार करा',
                'उपकरणे आणि सुविधा नियमितपणे निर्जंतुक करा',
                'आवश्यक असल्यास स्थानिक पशुवैद्यकीय अधिकाऱ्यांना निवेदन करा'
            ]
        },
        'severity': 'High',
        'urgency': 'High'
    },
    'foot-and-mouth': {
        'title': {
            'en': 'Foot and Mouth Disease',
            'hi': 'पैर और मुंह की बीमारी',
            'mr': 'पाय आणि तोंडाचा रोग'
        },
        'description': {
            'en': 'Your cow may be affected by Foot and Mouth Disease (FMD).',
            'hi': 'आपकी गाय पैर और मुंह की बीमारी (FMD) से प्रभावित हो सकती है।',
            'mr': 'आपली गाय पाय आणि तोंडाचा रोग (FMD) ने प्रभावित होऊ शकते.'
        },
        'suggestions': {
            'en': [
                'Immediately isolate the affected animal',
                'Contact a veterinarian urgently - FMD is highly contagious',
                'Report to veterinary authorities immediately (mandatory in most regions)',
                'Implement strict quarantine measures',
                'Disinfect all equipment, vehicles, and facilities',
                'Restrict movement of animals and people',
                'Provide soft, palatable feed and clean water',
                'Monitor for blisters on feet, mouth, and teats',
                'Separate affected animals from healthy ones',
                'Follow local regulations for FMD control'
            ],
            'hi': [
                'प्रभावित जानवर को तुरंत अलग करें',
                'तत्काल एक पशुचिकित्सक से संपर्क करें - FMD अत्यधिक संक्रामक है',
                'तुरंत पशुचिकित्सा अधिकारियों को रिपोर्ट करें (अधिकांश क्षेत्रों में अनिवार्य)',
                'सख्त संगरोध उपाय लागू करें',
                'सभी उपकरण, वाहन और सुविधाओं को कीटाणुरहित करें',
                'जानवरों और लोगों की आवाजाही प्रतिबंधित करें',
                'नरम, स्वादिष्ट चारा और स्वच्छ पानी प्रदान करें',
                'पैर, मुंह और थनों पर फफोले की निगरानी करें',
                'प्रभावित जानवरों को स्वस्थ जानवरों से अलग करें',
                'FMD नियंत्रण के लिए स्थानीय नियमों का पालन करें'
            ],
            'mr': [
                'प्रभावित प्राण्याला ताबडतोब वेगळे करा',
                'तातडीने पशुवैद्याशी संपर्क साधा - FMD अत्यंत संसर्गजन्य आहे',
                'ताबडतोब पशुवैद्यकीय अधिकाऱ्यांना निवेदन करा (बहुतेक प्रदेशांमध्ये अनिवार्य)',
                'कठोर संगरोध उपाय अंमलात आणा',
                'सर्व उपकरणे, वाहने आणि सुविधा निर्जंतुक करा',
                'प्राणी आणि लोकांची हालचाल प्रतिबंधित करा',
                'मऊ, चवदार खाद्य आणि स्वच्छ पाणी प्रदान करा',
                'पाय, तोंड आणि थनांवर फोडांचे निरीक्षण करा',
                'प्रभावित प्राण्यांना निरोगी प्राण्यांपासून वेगळे करा',
                'FMD नियंत्रणासाठी स्थानिक नियमांचे पालन करा'
            ]
        },
        'severity': 'Critical',
        'urgency': 'Critical'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(img_path):
    """Preprocess image for prediction"""
    # Import TensorFlow image processing here to avoid slow startup
    from tensorflow.keras.preprocessing import image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predict_disease(img_path):
    """Predict disease from image"""
    if model is None:
        return None, None, "Model not found. Please train the model first by running 'python train_model.py'"
    
    try:
        img_array = preprocess_image(img_path)
        predictions = model.predict(img_array, verbose=0)
        
        # Check if image is likely of a cow by examining confidence levels
        max_confidence = float(np.max(predictions[0]))
        confidence_threshold = 0.3  # 30% confidence threshold
        
        if max_confidence < confidence_threshold:
            return None, None, "Please upload a valid cow image. The uploaded image does not appear to be of a cow."
        
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Map index to class name - use index_to_class mapping if available
        if index_to_class and predicted_class_idx in index_to_class:
            predicted_class = index_to_class[predicted_class_idx]
        elif isinstance(class_names, list):
            predicted_class = class_names[predicted_class_idx] if predicted_class_idx < len(class_names) else 'unknown'
        else:
            # If class_names is a dict (from flow_from_directory), get the key by index
            class_list = list(class_names.keys())
            predicted_class = class_list[predicted_class_idx] if predicted_class_idx < len(class_list) else 'unknown'
        
        # Normalize class name (handle variations like 'foot-and-mouth' vs 'foot_and_mouth')
        predicted_class = predicted_class.replace('_', '-').lower()
        
        # Map common variations to standard names
        class_mapping = {
            'foot and mouth': 'foot-and-mouth',
            'foot_and_mouth': 'foot-and-mouth',
            'lumpy skin': 'lumpy',
            'lumpy_skin': 'lumpy',
            'lumpyskin': 'lumpy'
        }
        
        if predicted_class in class_mapping:
            predicted_class = class_mapping[predicted_class]
        
        # Ensure we return one of the valid classes
        valid_classes = ['healthy', 'lumpy', 'foot-and-mouth']
        if predicted_class not in valid_classes:
            # Try to find closest match
            for valid_class in valid_classes:
                if valid_class in predicted_class or predicted_class in valid_class:
                    predicted_class = valid_class
                    break
            else:
                predicted_class = 'healthy'  # Default to healthy if no match
        
        return predicted_class, confidence, None
    except Exception as e:
        error_msg = f"Error in prediction: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return None, None, error_msg

@app.route('/')
def index():
    # Check if model is available
    model_status = {
        'available': model is not None,
        'error': model_error
    }
    return render_template('index.html', model_status=model_status)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', 'en')  # Get language preference
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict disease
            predicted_class, confidence, error_msg = predict_disease(filepath)
            
            if predicted_class is None:
                error_message = error_msg if error_msg else 'Prediction failed. Please check if the model is trained.'
                return jsonify({'error': error_message}), 500
            
            # Get doctor suggestions in requested language
            disease_info = DOCTOR_SUGGESTIONS.get(predicted_class, DOCTOR_SUGGESTIONS['healthy'])
            suggestions = {
                'title': disease_info['title'].get(language, disease_info['title']['en']),
                'description': disease_info['description'].get(language, disease_info['description']['en']),
                'suggestions': disease_info['suggestions'].get(language, disease_info['suggestions']['en']),
                'severity': disease_info['severity'],
                'urgency': disease_info['urgency']
            }
            
            # Read image for base64 encoding
            with open(filepath, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Save prediction to MongoDB
            if client:
                prediction_doc = {
                    "prediction": {
                        "image_name": filename,
                        "disease": predicted_class,
                        "confidence": round(confidence * 100, 2),
                        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "appointment": None,
                    "status": "predicted"
                }
                predictions_collection.insert_one(prediction_doc)
                print(f"Prediction saved to MongoDB: {prediction_doc}")
            
            return jsonify({
                'success': True,
                'prediction': predicted_class,
                'confidence': round(confidence * 100, 2),
                'suggestions': suggestions,
                'image': f'data:image/jpeg;base64,{img_base64}'
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/appointment', methods=['POST'])
def book_appointment():
    """Handle doctor appointment booking"""
    try:
        data = request.get_json()

        # Extract prediction data
        prediction_data = {
            'image_name': data.get('imageName', ''),
            'disease': data.get('disease', ''),
            'confidence': data.get('confidence', 0.0),
            'uploaded_at': data.get('uploadedAt', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        # Extract appointment data
        appointment_data = {
            'cow_id': data.get('cowId', f"COW_{datetime.now().strftime('%Y%m%d%H%M%S')}"),  # Generate if not provided
            'owner_name': data.get('ownerName', ''),
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'preferred_date': data.get('preferredDate', ''),
            'preferred_time': data.get('preferredTime', ''),
            'urgency': data.get('urgency', 'normal'),
            'location': data.get('location', '')
        }

        print(f"Appointment booked: {appointment_data}")

        # Save appointment to MongoDB
        if client:
            appointment_doc = {
                "prediction": prediction_data,
                "appointment": appointment_data,
                "status": "pending"
            }
            appointments_collection.insert_one(appointment_doc)
            print(f"Appointment saved to MongoDB: {appointment_doc}")

        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully and data stored in MongoDB.',
            'cow_id': appointment_data['cow_id']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """Advanced chatbot endpoint for comprehensive cow disease information"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower().strip()

        if not user_message:
            return jsonify({
                'success': True,
                'response': "Hello! I'm here to help you with information about cow diseases, health, and care. What would you like to know?"
            })

        # Quick responses for common queries to make chatbot more responsive
        quick_responses = {
            'hello': "Hello! I'm your cow health assistant. How can I help you today?",
            'hi': "Hi there! I'm here to help with cow health information. What would you like to know?",
            'help': "I can help you with information about cow diseases, symptoms, treatment, and prevention. Try asking about 'lumpy skin disease', 'foot and mouth', or 'mastitis'.",
            'thanks': "You're welcome! Feel free to ask if you have more questions about cow health.",
            'thank you': "You're welcome! I'm here whenever you need help with cattle health concerns.",
            'bye': "Goodbye! Remember to monitor your cattle regularly and consult a veterinarian for any health concerns.",
            'goodbye': "Take care! Regular health monitoring is key to keeping your cattle healthy.",
            'what diseases': "Common cattle diseases include: Lumpy Skin Disease, Foot and Mouth Disease, mastitis, bovine respiratory disease, and bovine viral diarrhea. Ask me about any specific disease for more details.",
            'symptoms': "Different diseases show different symptoms. For example: LSD shows skin nodules and fever, FMD shows mouth blisters and lameness. Tell me which disease you're concerned about.",
            'prevention': "Disease prevention includes: proper vaccination, good hygiene, quarantine new animals, regular veterinary check-ups, and maintaining clean housing. Specific prevention varies by disease.",
            'treatment': "Treatment depends on the disease. Most involve supportive care, antibiotics for bacterial infections, and sometimes specific medications. Always consult a veterinarian for proper treatment.",
            'vaccine': "Vaccination is crucial for disease prevention. Common vaccines include those for LSD, FMD, BRD, and BVD. Consult your vet for a vaccination schedule suitable for your area.",
            'healthy': "A healthy cow should have: clear bright eyes, good appetite, normal body temperature (101.5-103.5°F), no abnormal discharges, normal breathing, and good body condition.",
            'feed': "Proper nutrition is essential. Cattle need good quality forage, balanced concentrates, minerals, and clean water. Consult a nutritionist for specific feed requirements.",
            'water': "Cattle need access to clean, fresh water at all times. Adult cattle drink 25-50 gallons per day depending on temperature and production level.",
            'milk': "Milk production depends on breed, age, nutrition, and health. Monitor for mastitis signs like abnormal milk or udder swelling. Consult a vet if production drops suddenly."
        }

        # Check for quick responses first
        user_lower = user_message.lower().strip()
        for key, response in quick_responses.items():
            if key in user_lower or user_lower in key:
                return jsonify({
                    'success': True,
                    'response': response
                })

        # Comprehensive knowledge base
        knowledge_base = {
            # Disease-specific information
            'lumpy_skin_disease': {
                'keywords': ['lumpy', 'lumpy skin', 'lumpy skin disease', 'lsd', 'nodules', 'skin nodules', 'lump', 'lumps', 'skin lump', 'skin disease'],
                'symptoms': "Lumpy Skin Disease (LSD) symptoms include: fever (104-106°F), loss of appetite, reduced milk production, skin nodules (1-5cm diameter), swelling of lymph nodes, nasal discharge, lacrimation (watering eyes), and depression.",
                'causes': "LSD is caused by the Lumpy Skin Disease Virus (LSDV), a member of the Poxviridae family. It's transmitted by blood-feeding insects like mosquitoes, flies, and ticks. The virus can also spread through contaminated feed, water, and direct contact with infected animals.",
                'treatment': "There is no specific antiviral treatment for LSD. Supportive care includes: isolation of affected animals, anti-inflammatory drugs (NSAIDs like flunixin meglumine), antibiotics for secondary infections, nutritional support, and good nursing care. Recovery usually takes 2-4 weeks.",
                'prevention': "Prevention measures: vaccination with live attenuated vaccines, vector control (insect repellents, proper housing), quarantine new animals for 28 days, maintain clean facilities, avoid mixing with infected herds, and report outbreaks immediately.",
                'severity': "LSD has a mortality rate of 1-3% in adult cattle, but can be higher in young animals. It's economically devastating due to reduced milk production and trade restrictions."
            },

            'foot_mouth_disease': {
                'keywords': ['foot', 'mouth', 'foot and mouth', 'fmd', 'blisters', 'lameness', 'hoof', 'feet', 'tongue', 'saliva', 'drooling'],
                'symptoms': "Foot and Mouth Disease (FMD) symptoms include: fever (104-106°F), blisters on feet, mouth, tongue, and teats, excessive salivation, lameness, reduced milk production, abortion in pregnant cows, and weight loss.",
                'causes': "FMD is caused by Aphthovirus from the Picornaviridae family. It spreads through direct contact with infected animals, contaminated feed/water, aerosols, and fomites. The virus survives in meat products and can travel long distances via wind.",
                'treatment': "No specific cure exists. Treatment is supportive: isolation, soft palatable feed, antiseptic mouthwashes, antibiotics for secondary infections, and pain management. Most animals recover in 2-3 weeks, but may become carriers.",
                'prevention': "Prevention: vaccination programs, strict biosecurity, quarantine (21 days), disinfection of premises, restriction of animal movement, and immediate reporting. FMD is a notifiable disease requiring government intervention.",
                'severity': "FMD is highly contagious with up to 100% morbidity. Mortality is low (1-5%) but causes massive economic losses through trade bans and reduced productivity."
            },

            'mastitis': {
                'keywords': ['mastitis', 'udder', 'milk', 'udder infection', 'teat', 'swollen udder', 'abnormal milk', 'milk quality'],
                'symptoms': "Mastitis symptoms: abnormal milk (watery, bloody, or pus-filled), swollen udder, heat in udder, pain during milking, reduced milk yield, fever, and lethargy.",
                'causes': "Caused by bacteria (Staphylococcus, Streptococcus, E. coli) entering through the teat canal. Risk factors: poor milking hygiene, teat injuries, overcrowding, and stress.",
                'treatment': "Treatment: intramammary antibiotics, anti-inflammatory drugs, frequent milking, warm compresses, and supportive care. Chronic cases may require udder flushing.",
                'prevention': "Prevention: proper milking hygiene, post-milking teat disinfection, regular udder checks, dry cow therapy, and maintaining clean housing."
            },

            'bovine_respiratory_disease': {
                'keywords': ['respiratory', 'breathing', 'cough', 'pneumonia', 'lung', 'brd', 'shipping fever', 'nasal discharge', 'runny nose'],
                'symptoms': "BRD symptoms: coughing, nasal discharge, fever, rapid breathing, depression, reduced appetite, and weight loss. Severe cases show labored breathing and cyanosis.",
                'causes': "Caused by viruses (BRSV, PI3, BVDV) and bacteria (Mannheimia, Pasteurella, Mycoplasma). Stress factors like weaning, transport, and weather changes predispose cattle to infection.",
                'treatment': "Treatment: antibiotics (oxytetracycline, tilmicosin), anti-inflammatory drugs, supportive care, and ensuring good ventilation and reduced stress.",
                'prevention': "Prevention: vaccination programs, proper ventilation, reduced stress during handling, good nutrition, and avoiding overcrowding."
            },

            'bovine_viral_diarrhea': {
                'keywords': ['bvd', 'viral diarrhea', 'bovine viral diarrhea', 'diarrhea', 'scours', 'loose stool', 'watery stool'],
                'symptoms': "BVD symptoms vary by form: acute - fever, diarrhea, nasal discharge, ulcers; chronic - poor growth, persistent infections; congenital - birth defects, weak calves.",
                'causes': "Caused by Pestivirus. Spread through direct contact, contaminated feed/water, and persistently infected (PI) carrier animals that shed virus lifelong.",
                'treatment': "No specific treatment. Supportive care: fluid therapy, antibiotics for secondary infections, and isolation. PI animals should be culled.",
                'prevention': "Prevention: vaccination, testing for PI animals, biosecurity, and culling of PI cattle."
            },

            # General health and care
            'nutrition': {
                'keywords': ['feed', 'nutrition', 'food', 'diet', 'grass', 'hay', 'silage', 'grain', 'eating', 'appetite', 'fodder'],
                'response': "Proper cow nutrition is crucial for health and productivity. A balanced diet should include: 60-70% roughage (grass, hay, silage), 30-40% concentrates (grains, protein supplements), minerals (calcium, phosphorus), and vitamins. Fresh water should always be available. Consult a nutritionist for specific herd requirements."
            },

            'vaccination': {
                'keywords': ['vaccine', 'vaccination', 'immunization', 'shot', 'injection', 'vaccinate', 'immunize'],
                'response': "Common cattle vaccinations include: Clostridial diseases (7-way, 8-way), Bovine Respiratory Disease complex, Bovine Viral Diarrhea, Infectious Bovine Rhinotracheitis, Leptospirosis, and Lumpy Skin Disease. Vaccination schedules vary by region and risk factors. Consult your veterinarian for a customized vaccination program."
            },

            'reproduction': {
                'keywords': ['pregnant', 'pregnancy', 'calving', 'birth', 'breeding', 'heat', 'estrus', 'calf', 'baby'],
                'response': "Cow reproduction: Estrus cycle is 18-24 days. Signs of heat include restlessness, mounting other cows, and clear vaginal discharge. Pregnancy lasts about 283 days. Calving assistance may be needed for first-calf heifers. Monitor for dystocia (difficult birth) and provide clean calving area."
            },

            'housing': {
                'keywords': ['housing', 'barn', 'shelter', 'bedding', 'stall', 'pen', 'shed', 'stable'],
                'response': "Good housing provides protection from weather, reduces stress, and prevents disease. Requirements: adequate space (80-100 sq ft per cow), good ventilation, dry bedding (straw, sand), clean water, and shade. Proper drainage prevents mud and standing water."
            },

            # Emergency situations
            'emergency': {
                'keywords': ['emergency', 'urgent', 'critical', 'help', 'dying', 'dead', 'severe', 'serious'],
                'response': "🚨 EMERGENCY SITUATION: If your cow shows severe symptoms like difficulty breathing, profuse bleeding, seizures, or is down and unable to rise, contact your veterinarian IMMEDIATELY or call emergency veterinary services. For reportable diseases (FMD, LSD), contact agricultural authorities right away."
            },

            # General questions
            'general_symptoms': {
                'keywords': ['symptom', 'sign', 'sick', 'ill', 'disease sign', 'not well', 'unwell'],
                'response': "Common disease signs in cattle: loss of appetite, fever, abnormal discharge, lameness, skin lesions, abnormal milk, coughing, diarrhea, weight loss, depression, or isolation from herd. Early detection is crucial - monitor your cattle daily and consult a vet at first signs of illness."
            },

            'general_prevention': {
                'keywords': ['prevent', 'prevention', 'avoid', 'stop', 'protect', 'protection'],
                'response': "Disease prevention strategies: regular veterinary check-ups, proper vaccination schedules, good nutrition and hygiene, quarantine new animals, vector control, clean water and feed, stress reduction, and prompt isolation of sick animals. Biosecurity is your best defense against disease outbreaks."
            },

            'veterinarian': {
                'keywords': ['vet', 'veterinarian', 'doctor', 'expert', 'professional', 'specialist'],
                'response': "Always consult a qualified veterinarian for diagnosis and treatment. They have the training and equipment to properly assess your cattle's health. Regular veterinary visits help prevent problems and catch issues early. Keep your vet's contact information handy and establish a relationship with them."
            },

            'milk_production': {
                'keywords': ['milk', 'milking', 'production', 'yield', 'dairy'],
                'response': "Milk production and quality depend on cow health, nutrition, and management. Normal milk production varies by breed and lactation stage. Monitor for mastitis signs: abnormal milk, swollen udder, or fever. Practice proper milking hygiene and consult a veterinarian if production drops suddenly."
            },

            'calf_care': {
                'keywords': ['calf', 'calves', 'baby', 'young', 'newborn', 'kid'],
                'response': "Newborn calf care: Ensure colostrum intake within first 6 hours for immunity. Monitor for navel infections, diarrhea, and pneumonia. Provide clean water, starter feed, and shelter. Vaccinate according to schedule and deworm regularly. Watch for signs of illness and consult vet promptly."
            },

            'fever': {
                'keywords': ['fever', 'temperature', 'hot', 'high temperature', 'pyrexia'],
                'response': "Normal cattle body temperature is 101.5-103.5°F (38.6-39.7°C). Fever indicates infection or inflammation. Common causes: viral/bacterial infections, heat stress, or inflammatory conditions. If fever persists over 103.5°F or accompanied by other symptoms, consult a veterinarian immediately."
            },

            'weight_loss': {
                'keywords': ['weight loss', 'thin', 'skinny', 'losing weight', 'underweight', 'emaciated'],
                'response': "Weight loss in cattle can indicate: poor nutrition, parasites, chronic disease, dental problems, or digestive issues. Check feed quality, deworm regularly, examine teeth, and monitor for other symptoms. Gradual weight loss requires veterinary evaluation to identify underlying cause."
            },

            'deworming': {
                'keywords': ['worm', 'deworm', 'parasite', 'deworming', 'anthelmintic'],
                'response': "Regular deworming is essential for cattle health. Common parasites: roundworms, tapeworms, liver flukes. Deworm calves at 2-3 months, then every 3-6 months. Use appropriate anthelmintics (ivermectin, fenbendazole) and rotate products to prevent resistance. Consult vet for deworming schedule."
            }
        }

        # Function to find best matching response
        def find_best_response(message):
            message_lower = message.lower()
            message_words = set(message_lower.split())

            best_match = None
            best_score = 0
            matched_category = None

            for category, info in knowledge_base.items():
                score = 0
                
                # Check keyword matches
                for keyword in info['keywords']:
                    keyword_lower = keyword.lower()
                    # Exact phrase match gets highest score
                    if keyword_lower in message_lower:
                        score += 10
                    # Word match gets lower score
                    elif keyword_lower in message_words:
                        score += 5
                    # Partial word match
                    elif any(keyword_lower in word for word in message_words):
                        score += 2

                if score > best_score:
                    best_score = score
                    best_match = info
                    matched_category = category

            return best_match, matched_category, best_score

        # Function to generate contextual response
        def generate_response(info, category, message):
            response_parts = []
            message_lower = message.lower()

            # Check for specific question types
            if any(word in message_lower for word in ['symptom', 'sign', 'show', 'look like', 'appear']):
                if 'symptoms' in info:
                    response_parts.append(f"**Symptoms of {category.replace('_', ' ').title()}:**\n{info['symptoms']}")

            if any(word in message_lower for word in ['cause', 'why', 'how get', 'spread', 'transmit', 'reason']):
                if 'causes' in info:
                    response_parts.append(f"\n**Causes of {category.replace('_', ' ').title()}:**\n{info['causes']}")

            if any(word in message_lower for word in ['treat', 'cure', 'medicine', 'heal', 'remedy', 'medication']):
                if 'treatment' in info:
                    response_parts.append(f"\n**Treatment for {category.replace('_', ' ').title()}:**\n{info['treatment']}")

            if any(word in message_lower for word in ['prevent', 'avoid', 'stop', 'protection', 'protect']):
                if 'prevention' in info:
                    response_parts.append(f"\n**Prevention of {category.replace('_', ' ').title()}:**\n{info['prevention']}")

            if any(word in message_lower for word in ['severe', 'bad', 'danger', 'mortality', 'serious', 'risk']):
                if 'severity' in info:
                    response_parts.append(f"\n**Severity of {category.replace('_', ' ').title()}:**\n{info['severity']}")

            # If no specific question type matched, provide general info
            if len(response_parts) == 0:
                if 'response' in info:
                    response_parts.append(info['response'])
                else:
                    # Provide comprehensive info
                    response_parts.append(f"**About {category.replace('_', ' ').title()}:**")
                    if 'symptoms' in info:
                        response_parts.append(f"\n**Symptoms:** {info['symptoms']}")
                    if 'treatment' in info:
                        response_parts.append(f"\n**Treatment:** {info['treatment']}")
                    if 'prevention' in info:
                        response_parts.append(f"\n**Prevention:** {info['prevention']}")

            return "\n".join(response_parts)

        # Find best response
        best_match, category, score = find_best_response(user_message)

        if best_match and score > 0:
            response_text = generate_response(best_match, category, user_message)
        else:
            # Fallback responses for unmatched queries
            if any(word in user_message for word in ['hello', 'hi', 'hey', 'greetings']):
                response_text = "Hello! I'm your cow health assistant. I can help you with information about cow diseases, symptoms, treatment, prevention, and general cattle care. What would you like to know?"
            elif any(word in user_message for word in ['thank', 'thanks']):
                response_text = "You're welcome! I'm here whenever you need help with cow health information. Feel free to ask about any cattle-related concerns."
            elif any(word in user_message for word in ['bye', 'goodbye', 'see you']):
                response_text = "Goodbye! Remember to monitor your cattle regularly and consult a veterinarian for any health concerns. Take care!"
            elif len(user_message) < 3:
                response_text = "Please provide more details about your question. I can help with cow diseases, symptoms, treatment options, prevention strategies, and general cattle care advice."
            else:
                response_text = "I'm here to help with cow health and disease information. I can answer questions about symptoms, causes, treatment, and prevention of common cattle diseases like Lumpy Skin Disease, Foot and Mouth Disease, mastitis, and more. Please rephrase your question or ask about a specific topic."

        # Add helpful follow-up suggestions
        if category and category in ['lumpy_skin_disease', 'foot_mouth_disease']:
            response_text += "\n\n⚠️ **Important:** This is a serious disease. Please consult a veterinarian immediately and report to local agricultural authorities if required."

        return jsonify({
            'success': True,
            'response': response_text
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'response': "I'm sorry, I encountered an error. Please try again or contact a veterinarian for urgent health concerns.",
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
