from flask import Flask, request, jsonify
from .database import get_db
from .models import KoboRecord
from .kobo_api import process_kobo_data
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/api/real-time-updates', methods=['POST'])
def webhook():
    data = request.json
    db = next(get_db())
    
    processed_data = process_kobo_data({'results': [data]})
    if processed_data:
        record = processed_data[0]
        kobo_id = record['kobo_id']
        existing_record = db.query(KoboRecord).filter(KoboRecord.kobo_id == kobo_id).first()
        
        if existing_record:
            for key, value in record.items():
                setattr(existing_record, key, value)
        else:
            new_record = KoboRecord(**record)
            db.add(new_record)
        
        db.commit()
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data format"}), 400

def register_webhook():
    INKOMOKO_REGISTER_WEBHOOK_URL = os.getenv('INKOMOKO_REGISTER_WEBHOOK_URL')
    REAL_TIME_POST_ENDPOINT_URL = os.getenv('REAL_TIME_POST_ENDPOINT_URL')
    url = INKOMOKO_REGISTER_WEBHOOK_URL
    payload = json.dumps({"url": REAL_TIME_POST_ENDPOINT_URL})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Failed to register webhook: {response.text}")
    