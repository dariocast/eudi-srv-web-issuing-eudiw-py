# Credential Offer Generation via API

## **🔹 Endpoint: `generateCredentialOffer`**
This API generates a **credential offer** for the EUDI Wallet, based on a signed or unsigned JSON Web Token (JWT).

---

## **📌 Request Details**

- **📍 URL:**  
  ```
  POST /generateCredentialOffer
  ```
- **📜 Content-Type:**  
  ```
  application/x-www-form-urlencoded
  ```

### **🔹 Request Parameters**
| **Parameter**    | **Type**    | **Required** | **Description** |
|-----------------|------------|-------------|----------------|
| `request`      | `string` (JWT) | ✅ Yes | The **JWT containing credential request data**. |
| `transaction_id` | `string`  | ❌ No  | An optional transaction ID. If **not provided**, one will be **generated automatically**. |

---

## **📌 JWT Structure**
### **✅ Example Payload (Valid Signed JWT)**
```json
{
  "exp": 1733980800, 
  "credentials": [
    {
      "credential_configuration_id": "it.unisa.credentials.elm_mdoc",
      "data": {
        "tin": "IT12345678901",
        //        ANY OTHER FIELD MARKED AS "user" IN THE "credential_supported" METADATA
      }
    }
  ]
}
```

---

## **📌 Response Details**

- **📜 Content-Type:**  
  ```
  application/json
  ```
- **📜 HTTP Status Codes:**
  - ✅ **200 OK** → Success
  - ❌ **400 Bad Request** → Missing JWT or Invalid JWT
  - ❌ **401 Unauthorized** → Expired JWT
  - ❌ **500 Internal Server Error** → Unexpected error

### **🔹 Example Response (Success)**
```json
{
  "credential_offer": {
    "credential_issuer": "https://issuer.example.com",
    "credential_configuration_ids": ["it.unisa.credentials.elm_mdoc"],
    "grants": {
      "urn:ietf:params:oauth:grant-type:pre-authorized_code": {
        "pre-authorized_code": "mocked_transaction_id",
        "tx_code": {
          "length": 5,
          "input_mode": "numeric",
          "description": "Please provide the one-time code.",
          "value": 12345
        }
      }
    }
  },
  "uri": "openid-credential-offer://credential_offer?credential_offer=...",
  "qr_code": "data:image/png;base64,iVBORw0KGg...",
  "tx_code": 12345,
  "transaction_id": "mocked_transaction_id"
}
```

---

## **📌 Error Responses**
### **🔴 400 Bad Request: Missing JWT**
```json
{
  "error": "Missing JWT request"
}
```
### **🔴 400 Bad Request: Invalid JWT**
```json
{
  "error": "Invalid JWT"
}
```
### **🔴 401 Unauthorized: Expired JWT**
```json
{
  "error": "JWT has expired"
}
```

---

## **📌 Example cURL Requests**

### **✅ 1. Valid JWT Request**
```bash
curl -X POST "http://localhost:5000/generateCredentialOffer" \
     -d "request=<VALID_SIGNED_JWT>" \
     -H "Content-Type: application/x-www-form-urlencoded"
```

### **✅ 2. Valid JWT with `transaction_id`**
```bash
curl -X POST "http://localhost:5000/generateCredentialOffer?transaction_id=test_tx_id" \
     -d "request=<VALID_SIGNED_JWT>" \
     -H "Content-Type: application/x-www-form-urlencoded"
```

### **❌ 3. Invalid JWT**
```bash
curl -X POST "http://localhost:5000/generateCredentialOffer" \
     -d "request=<INVALID_JWT>" \
     -H "Content-Type: application/x-www-form-urlencoded"
```

### **❌ 4. Expired JWT**
```bash
curl -X POST "http://localhost:5000/generateCredentialOffer" \
     -d "request=<EXPIRED_JWT>" \
     -H "Content-Type: application/x-www-form-urlencoded"
```

---

## **📌 Notes**
- The API **validates JWT signatures** **only if `hmac_secret` is set**.  
- If `hmac_secret` is **empty or missing**, the JWT is **decoded without signature verification**.  
- The response includes a **QR code** that can be scanned to process the credential offer.