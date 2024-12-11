import random

from flask import Flask, jsonify, request
from twilio.rest import Client

app = Flask(__name__)
otp_storage = {}

@app.route('/generate-sms-otp', methods=['POST'])
def generate_sms_otp():
    phone_number = request.json.get('phone_number')
    otp = random.randint(100000, 999999)
    otp_storage[phone_number] = otp

    # Sending SMS
    try:
        client = Client('***', '***')
        message = client.messages.create(
            body=f"Your Twilio verification code is: {otp}",
            from_='***',  # Twilio phone number
            to=phone_number
        )
        return jsonify({'message': 'OTP sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify-sms-otp', methods=['POST'])
def verify_sms_otp():
    phone_number = request.json.get('phone_number')
    otp = request.json.get('otp')
    if otp_storage.get(phone_number) == otp:
        return jsonify({'message': 'OTP verified successfully!'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
