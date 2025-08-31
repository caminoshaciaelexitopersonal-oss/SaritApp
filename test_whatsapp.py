import requests
import json

# The URL of the locally running webhook endpoint
url = "http://localhost:8000/api/v1/webhooks/whatsapp"

# A sample payload that mimics the structure of a message from WhatsApp
# Note: The phone numbers and IDs are examples.
sample_payload = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "1234567890",
            "changes": [
                {
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550001234",
                            "phone_number_id": "123456789012345"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Test User"
                                },
                                "wa_id": "15559876543"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15559876543",
                                "id": "wamid.HBgLMTU1NTk4NzY1NDMVCAASABoUM0VCMDlGNTYxM0Y5RDlEMzQyQjA3AA==",
                                "timestamp": "1678886400",
                                "text": {
                                    "body": "Hola, me gustaría saber más sobre sus planes de precios."
                                },
                                "type": "text"
                            }
                        ]
                    },
                    "field": "messages"
                }
            ]
        }
    ]
}

def test_webhook():
    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, json=sample_payload, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("Request successful!")
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_webhook()
