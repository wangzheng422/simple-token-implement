"""Module providing a singleton token service."""

from flask import Flask, jsonify, request
from threading import Lock, Timer
import sys
import os  # Import the os module

app = Flask(__name__)

# Initialize token variables and lock
# the program is designed to work with 1 tokens
# if a multiple tokens pool needed, it is better to define a class to manage the token pool and timeout
total_tokens = int(os.getenv('TOTAL_TOKENS', '1'))  # Default to 1 if not set
available_tokens = total_tokens
token_lock = Lock()
# issue_token_calls = 0  # Counter for issue_token calls

# Global variable to keep track of the timer
current_timer = None
timer_lock = Lock()  # Lock object to protect current_timer
# Read timer duration from environment variable, default to 1800 seconds if not set
timer_duration = int(os.getenv('TIMER_DURATION', '1800')) # 1800 seconds = 30 minutes


# Define a function to reset tokens and restart the timer
# in case of client dead of deleted, it will call issue_token, and will not call recycle_token
# for such case, we will reset num of token by checking, for a peroid of time, like 30mins
# if no call to issue_token, and the avilable token is zero, then reset the token to total token
def reset_tokens():
    global available_tokens
    with token_lock:
        if available_tokens == 0:
            available_tokens = total_tokens
            # available_tokens += 1
            print(f"Tokens reset to total tokens due to inactivity. Available tokens: {available_tokens}", file=sys.stdout)
        # Reset the issue_token_calls counter regardless of token reset
        # issue_token_calls = 0
    # Restart the timer
    start_timer()

def start_timer():
    global current_timer
    with timer_lock:  # Acquire the lock before accessing current_timer
        if current_timer is not None:
            # Cancel the existing timer
            current_timer.cancel()
            print("Previous timer cancelled.", file=sys.stdout)
        
        # Start a new timer
        current_timer = Timer(timer_duration, reset_tokens) # 1800 seconds = 30 minutes
        current_timer.start()
        print("New timer started.", file=sys.stdout)


def is_authorized():
    expected_password = "your_password_here"  # Replace with your password
    password = request.headers.get('X-API-PASSWORD', None)
    return password == expected_password


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

            start_timer()  # Restart the timer when a token is issued
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
    start_timer()  # Start the self-check timer when the application starts
    app.run(debug=True)