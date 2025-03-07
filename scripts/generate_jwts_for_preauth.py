# This is a utility script to generate all at once the required jwts to test the api
import copy

import jwt
import json
from datetime import datetime, timedelta, timezone
from app.app_config.config_secrets import hmac_secret

HMAC_SECRET = hmac_secret

# Define Payload (Common Data)
base_payload = {
    "credentials": [
        {
            "credential_configuration_id": "it.unisa.credentials.elm_mdoc",
            "data": {
                # TODO: Fix with actual values
                "tin": "IT12345678901"
            }
        }
    ]
}

# 1. Valid Signed JWT
valid_payload = copy.deepcopy(base_payload)  # Deep Copy to avoid mutation issues
valid_payload["exp"] = datetime.now(timezone.utc) + timedelta(days=365)
signed_jwt = jwt.encode(valid_payload, HMAC_SECRET, algorithm="HS256")

# 2. Valid Unsigned JWT (No Signature)
unsigned_jwt = jwt.encode(valid_payload, None, algorithm=None)

# 3. Expired JWT
expired_payload = copy.deepcopy(base_payload)  # Deep Copy again
expired_payload["exp"] = datetime.now(timezone.utc) - timedelta(days=1)
expired_jwt = jwt.encode(expired_payload, HMAC_SECRET, algorithm="HS256")

# 4. Invalid JWT (Wrong Secret)
invalid_jwt = jwt.encode(valid_payload, "wrong_secret", algorithm="HS256")

# Print Results in JSON Format
output = {
    "valid_signed_jwt": signed_jwt,
    "valid_unsigned_jwt": unsigned_jwt,
    "expired_jwt": expired_jwt,
    "invalid_jwt": invalid_jwt,
}

print(json.dumps(output, indent=4))
