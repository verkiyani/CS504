import io
from base64 import b64encode

import pyotp
import qrcode
from flask import Flask, jsonify, request

app = Flask(__name__)
shared_secrets = {}

@app.route('/generate-totp', methods=['POST'])
def generate_totp():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    # Generate a shared secret for the user
    secret = pyotp.random_base32()
    shared_secrets[username] = secret

    # Generate a QR code for the user
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="SecureApp")
    qr = qrcode.make(uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = b64encode(buffer.read()).decode('utf-8')
    totp = pyotp.TOTP(secret)
    otp = totp.now()

    return jsonify({'secret': secret, 'qr_code': img_str,"otp":otp}), 200

@app.route('/verify-totp', methods=['POST'])
def verify_totp():
    username = request.json.get('username')
    otp = request.json.get('otp')

    if not username or not otp:
        return jsonify({'error': 'Username and OTP are required'}), 400

    secret = shared_secrets.get(username)
    if not secret:
        return jsonify({'error': 'User not found'}), 404

    totp = pyotp.TOTP(secret)
    if totp.verify(otp):
        return jsonify({'message': 'OTP verified successfully!'}), 200
    else:
        return jsonify({'error': 'Invalid or expired OTP'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5002)
