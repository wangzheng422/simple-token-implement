"""Module providing a singleton token service."""

from flask import Flask, jsonify, request
from threading import Lock
import sys
import os  # Import the os module

app = Flask(__name__)

def is_authorized():
    expected_password = "your_password_here"  # Replace with your password
    password = request.headers.get('X-API-PASSWORD', None)
    return password == expected_password

# Initialize token variables and lock
# total_tokens = 1  # This can be configured to any number
total_tokens = int(os.getenv('TOTAL_TOKENS', '1'))  # Default to 1 if not set
available_tokens = total_tokens
token_lock = Lock()

@app.route('/issue_token', methods=['GET'])
def issue_token():
    if not is_authorized():
        return jsonify({"error": "Unauthorized"}), 401
    
    global available_tokens

    # Read 'info' parameter from the request
    info = request.args.get('info', 'No info provided')
    
    with token_lock:
        if available_tokens > 0:
            available_tokens -= 1
            message = {"message": "Token issued successfully.", "available_tokens": available_tokens, "info": info}
            status_code = 200
        else:
            message = {"message": "No tokens available.", "available_tokens": available_tokens, "info": info}
            status_code = 400

    # Display the message to the standard output
    print(f"Response: {message}", file=sys.stdout)

    return jsonify(message), status_code

@app.route('/recycle_token', methods=['GET'])
def recycle_token():
    if not is_authorized():
        return jsonify({"error": "Unauthorized"}), 401
    
    global available_tokens

    # Read 'info' parameter from the request
    info = request.args.get('info', 'No info provided')
    
    with token_lock:
        if available_tokens < total_tokens:
            available_tokens += 1
            message = {"message": "Token recycled successfully.", "available_tokens": available_tokens, "info": info}
            status_code = 200
        else:
            message = {"message": "All tokens are already available.", "available_tokens": available_tokens, "info": info}
            status_code = 400

    # Display the message to the standard output
    print(f"Response: {message}", file=sys.stdout)

    return jsonify(message), status_code

@app.route('/tokens', methods=['GET'])
def tokens():
    if not is_authorized():
        return jsonify({"error": "Unauthorized"}), 401
    
    return jsonify({"available_tokens": available_tokens}), 200

if __name__ == '__main__':
    app.run(debug=True)