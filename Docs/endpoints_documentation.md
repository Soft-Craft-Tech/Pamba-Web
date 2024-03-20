# Pamba Mobile Endpoint Docs

## 1. Auth

* ### Signup
Client signup endpoint

```javascript
    endpoint: POST /API/clients/signup
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Signup successful 
        "409 Conflict": Email or Phone number already exists.

    headers:
        X-API-KEY: <API_KEY>

    body: {
        "name": "***",
        "email": "***",
        "phone": "***",
        "password": "***"
    }
```

* ### Client Verification
Verify client with a verification code.

```javascript
    endpoint: POST /API/clients/verify-otp
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Verification Successful
        "404 Not found": Client not found.
        "400 Bad Request": Code expired/Not provided/Invalid

    headers:
        X-API-KEY: <API_KEY>

    body: {
        "email": "***",
        "otp": "******"
    }
```

* ### Client Login
Client login.

```javascript
    endpoint: POST /API/clients/login
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Login Successful, login token
        "404 Not found": Incorrect email.
        "401 Unauthorized": Incorrect pasword

    headers:
        X-API-KEY: <API_KEY>

    authorization: {
        "username": "***" //SHOULD BE THE CLIENT'S EMAIL ADDRESS,
        "password": "******"
    }
```

* ### Request Password Reset
Send password reset request.

```javascript
    endpoint: POST /API/clients/request-password-reset
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Reset token sent to email
        "404 Not found": Incorrect email.

    headers:
        X-API-KEY: <API_KEY>

    body: {
        "email": "***"
    }
```

* ### Reset Password
Reset your password with token sent via email

```javascript
    endpoint: POST /API/clients/reset-password/{token}
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Reset Successful
        "401 Unauthorized": Token invalid or expired
        "404 Not found": Not Found.

    headers:
        X-API-KEY: <API_KEY>

    body: {
        "password": "***"
    }
```

* ### Change Password
Client's change password

```javascript
    endpoint: POST /API/clients/reset-password/{token}
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Password Changed
        "401 Unauthorized": Old Password Incorrect

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>

    body: {
        "oldPassword": "***",
        "newPassword": "***"
    }
```

* ### Update Client's profile
Change the clients profile information

```javascript
    endpoint: POST /API/clients/update-profile
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Update successful, updated client_info
        "409 Confict": Email or phone already exists

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>

    body: {
        "email": "***",
        "phone": "***"
    }
```

* ### Resend Verification Code
Resend the client's verification token incase the one sent on signup is expired.

```javascript
    endpoint: POST /API/clients/resend-otp
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": OTP sent to email
        "404 Not Found": Client does not exist.
        "400 Bad Request": Account already verified

    headers:
        X-API-KEY: <API_KEY>

    body: {
        "email": "***"
    }
```

## 2. Businesses

* ### Fetch all Businesses
Fetch all Businesses listed.

```javascript
    endpoint: GET /API/clients/resend-otp
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Success, businesses

    headers:
        X-API-KEY: <API_KEY>

    body: {
        
    }
```

* ### Fetch Single Business
Fetch a single business given Business id

```javascript
    endpoint: GET /API/clients/business/{business_id}
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Success, business, services
        "400 Bad Request": Business not verified
        "404 Not Found": Business Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN-TOKEN>

    body: {
        
    }
```

## 3. Client Notifications

* ### Read Notification
Mark notification as read

```javascript
    endpoint: PUT /API/notifications/client/read/{notification_id}
    method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Notification Read, notification
        "400 Bad Request": Not allowed
        "404 Not Found": Notification Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>

    body: {
        
    }
```

* ### Fetch Notifications
Fetch notifications for a client

```javascript
    endpoint: GET /API/notifications/client/all
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Notifications

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        
    }
```
