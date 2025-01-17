import json
import base64
import requests

# Define the endpoint URL
url = "https://marmot-civil-gratefully.ngrok-free.app/credentialOfferReq2"

# Define the data to encode
data = {
    "credentials": [
        {
            "credential_configuration_id": "example_config_id_1",
            "data": {
                "given_name": "Maria Dolores",
                "family_name": "Delgado",
                "birth_date": "2020-01-25",
                "resident_city": "Napoli",
                "resident_country": "Italy",
                "resident_postal_code": "123456",
                "resident_street": "Corso Italia 1000",
                "issuing_country": "FC",
                "portrait": "base64_image_data",  # Replace with actual base64 image data if applicable
                "driving_privileges": [
                    {
                        "vehicle_category_code": "B",
                        "issue_date": "2025-01-01",
                        "expiry_date": "2030-01-01"
                    }
                ]
            }
        }
    ]
}

# Encode the data into a JWT-like format (base64 encoding)
encoded_data = base64.urlsafe_b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")

# Prepare the request payload
payload = {
    "request": encoded_data
}

# Make the POST request
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}

response = requests.post(url, headers=headers, data=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response Text:", response.text)
