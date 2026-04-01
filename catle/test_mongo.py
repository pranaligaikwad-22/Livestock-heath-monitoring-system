from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cow_disease_db']
    appointments_collection = db['appointments']
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    client = None

if client:
    # Test insert
    test_doc = {
        "prediction": {
            "image_name": "cow1.jpg",
            "disease": "lumpy",
            "confidence": 0.93,
            "uploaded_at": "2026-01-15 12:10:45"
        },
        "appointment": {
            "cow_id": "COW_102",
            "owner_name": "Ramesh Patil",
            "phone": "9876543210",
            "email": "ramesh@gmail.com",
            "preferred_date": "2026-01-18",
            "preferred_time": "10:30 AM",
            "urgency": "High",
            "location": "Pune, Maharashtra"
        },
        "status": "pending"
    }
    result = appointments_collection.insert_one(test_doc)
    print(f"Document inserted with ID: {result.inserted_id}")

    # Check if collection exists
    collections = db.list_collection_names()
    print(f"Collections in database: {collections}")

    # Find the document
    doc = appointments_collection.find_one({"appointment.cow_id": "COW_102"})
    if doc:
        print(f"Found document: {doc}")
    else:
        print("Document not found")
else:
    print("Client is None, cannot test")
