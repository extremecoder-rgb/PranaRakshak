# PranaRakshak - Indianapolis Public Safety WhatsApp Chatbot

PranaRakshak is a WhatsApp-based chatbot designed to provide Indianapolis residents with instant access to critical public safety information, emergency alerts, and local resources. Using advanced natural language processing powered by Google's Gemini AI, PranaRakshak delivers accurate, location-specific safety information 24/7.

[![Watch the demo](https://img.youtube.com/vi/_F1k9MnMIWw/hqdefault.jpg)](https://youtube.com/shorts/_F1k9MnMIWw)

## Features

- **Real-time Emergency Information**: Get instant updates about tornado warnings, floods, power outages, and other emergencies
- **Location-Specific Responses**: Provide your ZIP code for targeted information about your area
- **Emergency Shelter Locations**: Find nearby emergency shelters and contact information
- **Power Outage Updates**: Get real-time information about power outages and restoration status
- **Heat Wave Safety**: Access cooling center locations and heat safety tips
- **Emergency Contacts**: Quick access to important local emergency numbers
- **Message Logging**: Secure logging of all interactions for quality assurance
- **AI-Powered Responses**: Enhanced responses using Google's Gemini AI for natural conversation

## Prerequisites

- Python 3.7+
- Twilio account with WhatsApp sandbox enabled
- Google Gemini API key
- Flask web framework

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pepo.git
   cd PranaRakshak
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  
   .venv\Scripts\activate    
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file with the following variables:
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
   GEMINI_API_KEY=your_gemini_api_key
   PORT=5000
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Use ngrok to create a public URL:
   ```bash
   ngrok http 5000
   ```

3. Configure your Twilio WhatsApp sandbox with the ngrok URL:
   - Add `/bot` to your ngrok URL (e.g., `https://your-ngrok-url.ngrok.io/bot`)
   - Set this as your WhatsApp webhook URL in the Twilio console

## Customizing Responses

Edit the `responses.json` file to customize the bot's responses for different scenarios. The file contains predefined responses for common emergency situations and can be extended as needed.

## Deployment

For production deployment:

1. Set up a production server (e.g., AWS, DigitalOcean)
2. Configure a production-grade WSGI server (e.g., Gunicorn)
3. Set up HTTPS using a reverse proxy (e.g., Nginx)
4. Configure environment variables securely
5. Set up monitoring and logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Twilio for WhatsApp API integration
- Google for Gemini AI API
- Indianapolis Emergency Services for information and support
