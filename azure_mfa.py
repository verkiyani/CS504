from azure.identity import UsernamePasswordCredential
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        credential = UsernamePasswordCredential(
            client_id="***",
            tenant_id="***",
            username=username,
            password=password
        )
        token = credential.get_token("https://graph.microsoft.com/.default")
        return jsonify({'message': 'Authentication successful!', 'token': token.token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5003)
