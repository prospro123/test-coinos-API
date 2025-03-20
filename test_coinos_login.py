import requests
import json

def create_invoice(token, amount, invoice_type="lightning", webhook=None, secret=None):
    url = "https://coinos.io/api/invoice"
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
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
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error creating invoice. Status Code: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def test_coinos_login():
    url = "https://coinos.io/api/login"
    headers = {
        "content-type": "application/json"
    }
    data = {
        "username": "aidemo",
        "password": "notvipco"
    }

    try:
        # First get the token
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            token = data['token']
            
            # Now get account details
            auth_headers = {
                "Authorization": f"Bearer {token}",
                "content-type": "application/json"
            }
            
            # Get account details
            me_url = "https://coinos.io/api/me"
            me_response = requests.get(me_url, headers=auth_headers)
            
            if me_response.status_code == 200:
                account_data = me_response.json()
                print("\nAccount Details:")
                print("-" * 50)
                print(f"Username: {account_data['username']}")
                print(f"Balance: {account_data['balance']} {account_data['currency']}")
                print(f"Supported Currencies: {', '.join(account_data['currencies'])}")
                print(f"Account ID: {account_data['id']}")
                print(f"Public Key: {account_data['pubkey']}")
                print("-" * 50)
                
                # Create a test invoice
                print("\nCreating Test Invoice:")
                print("-" * 50)
                invoice = create_invoice(token, 1000, "lightning")
                if invoice:
                    print("Invoice created successfully!")
                    print(json.dumps(invoice, indent=2))
            else:
                print(f"Error getting account details. Status Code: {me_response.status_code}")
        else:
            print(f"Login failed. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_coinos_login() 