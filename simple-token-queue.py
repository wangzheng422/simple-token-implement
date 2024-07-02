from queue import Queue, Empty
from threading import Thread
import time

class TokenService:
    def __init__(self, max_tokens):
        self.available_tokens = Queue(max_tokens)
        for _ in range(max_tokens):
            self.available_tokens.put('token')  # Add a token to the queue

    def acquire_token(self):
        try:
            return self.available_tokens.get(block=False)  # Attempts to get a token without blocking
        except Empty:
            return False  # Returns False if no tokens are available

    def release_token(self, token):
        self.available_tokens.put(token)  # Release the token back to the pool