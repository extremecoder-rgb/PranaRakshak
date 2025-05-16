import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from twilio.rest import Client
from dotenv import load_dotenv
import requests


load_dotenv()

required_env_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER', 'GEMINI_API_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
    logger.info("Twilio client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {str(e)}")
    raise


def load_responses():
    try:
        with open('responses.json', 'r', encoding='utf-8') as file:
            responses = json.load(file)
            if not responses:
                logger.warning("responses.json is empty")
            return responses
    except FileNotFoundError:
        logger.error("responses.json file not found")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in responses.json: {str(e)}")
        return {}
    except Exception as e:
        logger.error(f"Error loading responses.json: {str(e)}")
        return {}

def log_message(phone_number, message, response):
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phone_number": phone_number,
            "message": message,
            "response": response
        }
        
        try:
            with open('message_logs.json', 'r') as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
            
        logs.append(log_entry)
        
        with open('message_logs.json', 'w') as file:
            json.dump(logs, file, indent=4)
            
        logger.info(f"Logged message from {phone_number}")
    except Exception as e:
        logger.error(f"Error logging message: {str(e)}")


def gemini_chat(prompt, location=None):
    try:
        if not GEMINI_API_KEY:
            logger.warning("Gemini API key not found, using fallback responses")
            return None
            
      
        if location:
            prompt = f"For Indianapolis area {location}: {prompt}"
        else:
            prompt = f"For Indianapolis residents: {prompt}"
            
       
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                if 'content' in result['candidates'][0] and 'parts' in result['candidates'][0]['content']:
                    parts = result['candidates'][0]['content']['parts']
                    if parts and 'text' in parts[0]:
                        return parts[0]['text']
        
        logger.warning(f"Gemini API call failed with status code: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        return None


def get_fallback_response(message):
    responses = load_responses()
    message = message.lower()
    
   
    for intent, response in responses.items():
        if intent.lower() in message:
            return response
    
   
    return responses.get("default", "I'm sorry, I couldn't understand your request. Please try asking about tornado warnings, shelters, power outages, evacuation info, heatwave tips, or emergency contacts.")


def extract_location(message):
    
    import re
    zip_match = re.search(r'\b(\d{5})\b', message)
    if zip_match:
        return zip_match.group(1)
    
   
    indy_areas = ["downtown", "broad ripple", "fountain square", "speedway", "castleton", "irvington"]
    for area in indy_areas:
        if area.lower() in message.lower():
            return area
    
    return None

@app.route('/bot', methods=['POST'])
def bot():
    try:
        
        if not request.values:
            logger.error("No form data in request")
            return jsonify({"status": "error", "message": "Invalid request"}), 400
            
        
        incoming_msg = request.values.get('Body', '').strip()
        sender_phone = request.values.get('From', '')
        
        if not incoming_msg or not sender_phone:
            logger.error("Missing required message parameters")
            return jsonify({"status": "error", "message": "Missing message parameters"}), 400
        
        logger.info(f"Received message from {sender_phone}: {incoming_msg}")
        
      
        location = extract_location(incoming_msg)
        
     
        response = gemini_chat(incoming_msg, location)
        
       
        if not response:
            response = get_fallback_response(incoming_msg)
        
        
        if len(response) > 1600:  
            response = response[:1600] + "..."
        
        
        twilio_client.messages.create(
            body=response,
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=sender_phone
        )
        
        
        log_message(sender_phone, incoming_msg, response)
        
        return jsonify({"status": "success"}), 200
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)