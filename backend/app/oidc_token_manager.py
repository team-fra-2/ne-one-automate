import time

import requests


class OIDCTokenManager:
    def __init__(self, token_url, client_id, client_secret, scope=""):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.token = None
        self.token_expiry = None

    def get_token(self):
        if self.token is None or time.time() > self.token_expiry:
            self.fetch_token()
        return self.token

    def fetch_token(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.scope is not None and self.scope != "":
            payload["scope"] = self.scope
        response = requests.post(self.token_url, data=payload)
        response.raise_for_status()
        token_response = response.json()
        self.token = token_response["access_token"]
        # Adjust expiry time slightly earlier to account for any delays
        self.token_expiry = time.time() + token_response["expires_in"] - 60
