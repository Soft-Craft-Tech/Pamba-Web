# Pamba Mobile Endpoint Docs

# 1. Auth

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
    endpoint: POST /API/clients/change-password
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

# 2. Businesses

* ### Fetch all Businesses
Fetch all activated Businesses.

```javascript
    endpoint: GET /API/businesses/all-businesses
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
    endpoint: GET /API/businesses/{business_id}
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

* ### Fetch Service Businesses
Fetch Businesses associated with a certain service

```javascript
    endpoint: GET /API/businesses/service-businesses/{service_id}
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Businesses
        "404 Not Found": Service Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN-TOKEN>

    body: {
        
    }
```

# 3. Client Notifications

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

# 4. Appointments

* ### Book Appointment
Client's appointment Booking

```javascript
    endpoint: POST /API/appointments/book
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Booking Successful.
        "400 Bad Request": Double Booking. Another Appointment scheduled at the same time.
        "401 Unauthorized": Account not verified.
        "404 Not Found": The shop/business does not exist.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "date": "***",
        "time": "***",
        "comment": "***",
        "provider": "***" // Refers to the ID if the business/shop.
    }
```

* ### Reschedule Appointment
Reschedule client's appointments.

```javascript
    endpoint: POST /API/appointments/reschedule/{appointment_id}
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Resheduling Successful.
        "400 Bad Request": Appointment is already completed.
        "401 Unauthorized": Not allowed
        "404 Not Found": The shop/business does not exist.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "date": "***",
        "time": "***"
    }
```

* ### Cancel Appointment
Cancel Appointment

```javascript
    endpoint: POST /API/appointments/cancel/{appointment_id}
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Cancellation Successful.
        "400 Bad Request": Appointment is already completed.
        "401 Unauthorized": Not allowed
        "404 Not Found": The shop/business does not exist.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "comment": "***" //Reason for cancellation
    }
```

* ### Client's Appointments
All appointments for a certain client.

```javascript
    endpoint: GET /API/appointments/my-appointments
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Appointments.
        "404 Not Found": No appointment booked yet.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        
    }
```

# 5. Expenses

* ### New Expense Record
Create new expense.

```javascript
    endpoint: POST /API/expenses/record-expense
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "201 Created": message, expense.
        "400 Bad Request": message: Not allowed, Account doesn't exist

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "expenseTitle": ""
        "expenseAmount": int
        "description": ""
        "accountID": int
    }
```

* ### Delete Expense
Delete Business's expense given ID

```javascript
    endpoint: DELETE /API/expenses/delete-expense/{expense_id}
    method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": message, deleted.
        "400 Bad Request": message: Incorrect password
        "404 Not Found": message: Expense Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "password": "xxxx"
    }
```

* ### Update Business Expense

```javascript
    endpoint: PUT /API/expenses/update-expense/{expense_id}
    method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": message, updated //Updated expense.
        "400 Bad Request": message: Incorrect password
        "404 Not Found": message: Expense Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "expenseTitle": "xxx"
        "expenseAmount": "xxx"
        "description": "xxx"
        "accountID": "xxx"
        "password": "xxxx"
    }
```

* ### Fetch Business Expenses
Fetch all Expenses associated with the business.

```javascript
    endpoint: GET /API/expenses/my-expenses
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": expenses //empty array if null

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {}
```

* ### Fetch a single Expense

```javascript
    endpoint: GET /API/expenses/expense/{expense_id}
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": expenses //empty array if null
        "400 Bad Request": message: Not Allowed //If expense doen't belong to business requesting.
        "404 Not Found": message: Expense Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {}
```