import random
import smtplib

from flask import Flask, jsonify, request

app = Flask(__name__)
otp_storage = {}

@app.route('/generate-email-otp', methods=['POST'])
def generate_email_otp():
    email = request.json.get('email')
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp

    # Sending email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('***@gmail.com', '***')
        message = f"Your OTP is {otp}"
        server.sendmail('***@gmail.com', email, message)
        server.quit()
        return jsonify({'message': 'OTP sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify-email-otp', methods=['POST'])
def verify_email_otp():
    email = request.json.get('email')
    otp = request.json.get('otp')
    if otp_storage.get(email) == otp:
        return jsonify({'message': 'OTP verified successfully!'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 400

if __name__ == '__main__':
    app.run(debug=True)
