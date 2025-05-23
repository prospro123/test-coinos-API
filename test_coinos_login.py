import requests
import json
from typing import Optional, Dict, Any

class CoinosAPI:
    def __init__(self, username: str, password: str):
        self.base_url = "https://coinos.io/api"
        self.token = None
        self.username = username
        self.password = password
        self.headers = {
            "content-type": "application/json"
        }

    def login(self) -> bool:
        """Login to Coinos API and get authentication token."""
        url = f"{self.base_url}/login"
        data = {
            "username": self.username,
            "password": self.password
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                self.token = response.json()['token']
                self.headers["Authorization"] = f"Bearer {self.token}"
                return True
            else:
                print(f"Login failed. Status Code: {response.status_code}")
                print("Response:", response.text)
                return False
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False

    def get_account_details(self) -> Optional[Dict[str, Any]]:
        """Get current account details."""
        if not self.token:
            print("Not logged in. Please login first.")
            return None

        try:
            response = requests.get(f"{self.base_url}/me", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting account details. Status Code: {response.status_code}")
                print("Response:", response.text)
                return None
        except Exception as e:
            print(f"Error getting account details: {str(e)}")
            return None

    def create_invoice(self, amount: int, invoice_type: str = "lightning", 
                      webhook: Optional[str] = None, secret: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new invoice.
        
        Args:
            amount: Amount in satoshis
            invoice_type: "lightning" or "bitcoin"
            webhook: Optional webhook URL for payment notifications
            secret: Optional secret for webhook verification
        """
        if not self.token:
            print("Not logged in. Please login first.")
            return None

        url = f"{self.base_url}/invoice"
        data = {
            "invoice": {
                "amount": amount,
                "type": invoice_type
            }
        }

        # Add optional parameters if provided
        if webhook:
            data["invoice"]["webhook"] = webhook
        if secret:
            data["invoice"]["secret"] = secret

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creating invoice. Status Code: {response.status_code}")
                print("Response:", response.text)
                return None
        except Exception as e:
            print(f"Error creating invoice: {str(e)}")
            return None

def main():
    # Initialize API client
    api = CoinosAPI("aidemo", "notvipco")

    # Login
    if not api.login():
        print("Failed to login. Exiting...")
        return

    # Get account details
    print("\nAccount Details:")
    print("-" * 50)
    account = api.get_account_details()
    if account:
        print(f"Username: {account['username']}")
        print(f"Balance: {account['balance']} {account['currency']}")
        print(f"Supported Currencies: {', '.join(account['currencies'])}")
        print(f"Account ID: {account['id']}")
        print(f"Public Key: {account['pubkey']}")
        print("-" * 50)

        # Create a test Lightning invoice
        print("\nCreating Test Lightning Invoice:")
        print("-" * 50)
        invoice = api.create_invoice(1000, "lightning")
        if invoice:
            print("Invoice created successfully!")
            print(json.dumps(invoice, indent=2))

        # Create a test Bitcoin invoice
        print("\nCreating Test Bitcoin Invoice:")
        print("-" * 50)
        invoice = api.create_invoice(1000, "bitcoin")
        if invoice:
            print("Invoice created successfully!")
            print(json.dumps(invoice, indent=2))

if __name__ == "__main__":
    main() 