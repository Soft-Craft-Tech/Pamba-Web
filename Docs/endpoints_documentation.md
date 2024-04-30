# Pamba Mobile Endpoint Docs

# 1. Auth Client

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

# 2. Business Auth
### signup businesses
signup a business
```javascript
    endpoint: GET API/businesses/signup
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Business created
        "400 Bad Request": Business already exists
        "409" : Email/Phone already exists
    headers:
        X-API-KEY: <API_KEY>
    body : {
}
```
* ### login into a business account 
login into a business account
```javascript
     endpoint: GET API/businesses/login
     method: POST
     Content Type: "Application/Json"
     Status Codes: 
        "200 OK": Business logged in successfully
        " 404" : incorrect Email or password
    
    headers : 
         X-API-KEY: <API_KEY>
    body : {
}
```
* ### request password reset
request password reset for the business account
```javascript
    endpoint : GET API/businesses/request-password-reset
    method : POST
    Content Type : "Application/json"
    Status Codes:
      "200": Reset link has been sent to your email
      " 404": Email does'nt exist
    headers : 
      X-API-Key : <API_KEY>
    body : {
}
    
```
* ### reset-password
reset password
```javascript
     endpoint : GET API/businesses/reset-password{business_id}
     method : PUT
     Content Type : "Application/Json"
     Status Codes : 
       "200" : password reset sucessful
       "400" : reset token is invalid or expired
     headers : 
       X-API-Key : <API_KEY>
     body : {
}
```
* ### activate account
activate  business account
```javascript

     endpoint : GET API/business/activate-account/<token>
     method : POST
     Status Code : 
       "200 " : Success
       "400" : Token Invalid or Expired
       "404" : Not Found
     headers : 
       X-API-Key : <API_KEY>
     body : {
}
```
* ### resend activation token
resend activation token
```javascript
     endpoint : GET API/businesses/resend-activation-token
     method : POST
     Content Type : "Application/Json"
     Status Code : 
       "200 " : activation token sent to your email
       "400" : account already activated
     headers : 
       X-API-Key : <API_KEY>
     body : {
}
```

# 3. Businesses
* ###  update profile
 update profile

```javascript

     endpoint : GET  API/businesses/update
     method : PUT
     Content Type : "Application/Json"
     Status Code : 
       "200 " : Update Successful
       "401" : Incorrect password
       "409" : Phone number already exists/Email already exists  
     headers : 
       X-API-Key : <API_KEY>
     body : {
         "name": "Updated Business Name",
         "email": "updated@example.com",
         "phone": "1234567890",
         "city": "Updated City",
         "location": "Updated Location",
         "description": "Updated business description.",
         "mapUrl": "https://maps.google.com/...",
         "password": "currentPassword123"
}
```
* ### change password
Allow the business owner to change their password
change password

```javascript

     endpoint : GET API/businesses/change-password
     method : PUT
     Content Type : "Application/Json"
     Status Code : 
       "200 " : Success! Password has been changed
       "401" : Old password is incorrect
     headers : 
       X-API-Key : <API_KEY>
     body : {
         "oldPassword": "currentPassword123",
         "newPassword": "newPassword456"
}
```


* ###assign services
assign services to a business

```javascript

     endpoint : GET API/business/assign-services
     method : POST
     Content Type : "Application/Json"
     Status Code : 
       "200 " : Services have been Added
       "400" : No service to be added
       "500" : An error occurred please try again
     headers : 
       X-API-Key : <API_KEY>
     body : {
         "services": [
             {
                 "id": "service_id_1",
                 "price": "service_price_1"
             },
             {
                 "id": "service_id_2",
                 "price": "service_price_2"
             }
         ]
}
```
* ### remove service
remove service from a business account

```javascript

     endpoint : GET API/business/remove-service
     method : POST
     Content Type : "Application/Json"
     Status Code : 
       "200 " : Service removed
       "404" : Service not found
     headers : 
       X-API-Key : <API_KEY>
     body : {
         "serviceId": "service_id_to_remove"
}
```
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
* ### get business analytics
get business analytics
```javascript

     endpoint : GET /business/analysis
     method : GET
     Status Code : 
       "200 " : Analysis data
     headers : 
       X-API-Key : <API_KEY>
     body : {
}
```
* ### Fetch Single Business
Fetch a single business given Business id

```javascript
    endpoint: GET /API/businesses/<string:slug>
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Success, business, services
        "400 Bad Request": Business not verified
        "404 Not Found": Business Not found

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN-TOKEN>
    URL Parameters:
        slug: string (unique identifier for the business)

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
### upload-profile-img
```javascript
    endpoint: GET API/business/upload-profile-img
    method : PUT
    Content Type: "Application/Json"
    Status Codes: 
        "200 OK": succesfully uploaded profile-img
    headers:
        X-API-KEY: <API_KEY>
        body: {
        profile_img: <FILE>
    }
```
### update-description
```javascript
     endpoint: GET API/business/update-description
     method: PUT
     Content Type: "Application/Json"
     Status Codes: 
        "200 OK":updated successful
        " 400 Invalid Request": No description added
     headers:
         X-API-KEY: <API_KEY>
         x-access-token: <LOGIN-TOKEN>

     body: {

     }
```
### profile-completion-status
```javascript
     endpoint: GET API/business/profile-completion-status
     method: GET
     Content Type: "Application/Json"
     Status Codes: 
         "200 OK": profile completion status success
     headers:
         X-API-KEY: <API_KEY>
         x-access-token: <LOGIN-TOKEN>

     body: {

     }
```

### fetch-business-category
```javascript
     endpoint: GET /API/business/fetch-business-category
     method : GET
     Content Type: "Application/Json"
     Status Codes: 
        "200 OK": businesses categories
        "404 Not Found": category Not found

     headers:
         X-API-KEY: <API_KEY>
         x-access-token: <LOGIN-TOKEN>

     body: {
         
     }
```
* ### Add Business Hours

### Add operating hours for the logged-in business.

```javascript

    endpoint: GET API/businesess/business-hours
    method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Success
        "401 Unauthorized": Unauthorized

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>

    body: {
        "weekdayOpening": "HH:MM",
        "weekdayClosing": "HH:MM",
        "weekendOpening": "HH:MM",
        "weekendClosing": "HH:MM"
    }

```
# 4. Client Notifications

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
#### Client's appointment Booking

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

### Book an appointment from the web 
```javascript
    endpoint: GET API/appointments/book/web-appointments
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "201 Created": Appointment Booked Successfully
        "404 Not Found": The service you are booking is unavailable or Business not found
        "400 Bad Request": Our premises are not open at the picked time and day

    body: {
        "date": "DD-MM-YYYY",
        "time": "HH:MM",
        "business": "Business ID",
        "service": "Service ID",
        "email": "Client's email",
        "phone": "Client's phone number"
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
# 6. Inventory
*  ### fetch all Inventory records for the businessdescription: <DESCRIPTION>
```javascript
    Endpoint: GET /API/inventory/business-inventory
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 Ok": Inventory

    Headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### Record new inventory
```javascript
      Endpoint: POST /API/inventory/record-inventory
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "201 Created": Message, Inventory.
    
    Headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### Delete Inventory
Delete Inventory with id
```javascript
      Endpoint: DELETE /API/inventory/delete-inventory/{inventory_id}
    Method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": Message, Deleted.
        "401 Unauthorized": Message: Incorrect password
        "404 Not Found": Message: Record Not found

    Headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "password": "xxxx"
    }
```
* #### Update Inventory status
```javascript
     Endpoint: PUT /API/inventory/update-status/{inventory_id}
    Method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": Message, Updated //Updated inventory.
        "400 Bad Request": Message: Status not recognized
        "401 Unauthorized": Message: Not allowed
        "404 Not Found": Message: Record Not found

    Headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "status": "New Status"
    }
```
# 7. Ratings
* ### Add rating to a business
```javascript
         Endpoint: POST /API/ratings/new
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": Message, Rating has been posted.
        "404 Not Found": Message: Business doesn't exist

    Headers:
        X-API-KEY: <API_KEY>
    Body: {
        "rating": <int>,
        "businessID": <int>
    }
```
# 8. Review
* ### Create Review 
```javascript
      Endpoint: POST /API/reviews/create
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 Created": Message, Review has been posted.
        "404 Not Found": Message: Business doesn't exist

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "message": "Review Message",
        "businessID": <int>
    }
```
# 9. Sales
* ### fetch a single sale 
```javascript
     Endpoint: GET /API/sales/{sale_id}
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Sale details.
        "401 Unauthorized": Message: Not allowed
        "404 Not Found": Message: Sale not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### fetch all sales
```javascript
    Endpoint: GET /API/sales/all
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Sales.

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### Record New sale 
```javascript
    Endpoint: POST /API/sales/add-sale
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message, Sale Added.
        "400 Bad Request": Message: You need to activate your account first. Or We are not offering this service at the moment.

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "paymentMethod": "Payment Method",
        "description": "Description",
        "serviceId": <int>
    }
```
* ### Update sale
``` javascript
      Endpoint: PUT /API/sales/update/{sale_id}
    Method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Sale updated.
        "400 Bad Request": Message: Incorrect password or Invalid sale ID
        "401 Unauthorized": Message: Not allowed
        "404 Not Found": Message: Sale not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "paymentMethod": "New Payment Method",
        "description": "New Description",
        "password": "xxxx"
    }
```
* ### Delete a sale
```javascript
    Endpoint: DELETE /API/sales/delete/{sale_id}
    Method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Sale deleted.
        "400 Bad Request": Message: Incorrect password
        "404 Not Found": Message: Not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "password": "xxxx"
    }
```
# 10. staff
* ### fetch single staff
```javascript
    Endpoint: GET /API/staff/single/{staff_id}
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Staff details.
        "401 Unauthorized": Message: Not allowed
        "404 Not Found": Message: Staff not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### fetch all staffs
```javascript
   Endpoint: GET /API/staff/all
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": All staff records.

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### update staff info
```javascript
      Endpoint: PUT /API/staff/update-staff/{staff_id}
    Method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Updated.
        "401 Unauthorized": Message: Incorrect password
        "404 Not Found": Message: Staff not found
        "409 Conflict": Message: Phone number already exists

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "password": "xxxx",
        "phone": "New Phone Number",
        "role": "New Role"
    }
```
* ### delete a staff member
```javascript
    Endpoint: DELETE /API/staff/delete-staff/{staff_id}
    Method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Staff deleted.
        "401 Unauthorized": Message: Incorrect password
        "404 Not Found": Message: Staff not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "password": "xxxx"
    }
```
# 11. Business-Notifications
* ### create Business notification
```javascript
      Endpoint: POST /API/notifications/businesses/create
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "201 Created": Message: Notification sent.

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "title": "Notification Title",
        "message": "Notification Message",
        "businessID": <int>
    }
```
* ### mark Business Notifications as Read
```javascript
      Endpoint: PUT /API/notifications/business/read/{notification_id}
    Method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Notification Read.
        "401 Unauthorized": Message: Not Allowed
        "404 Not Found": Message: Not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### Delete Business Notifications
```javascript
        Endpoint: DELETE /API/notifications/business/delete/{notification_id}
    Method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Deleted.
        "401 Unauthorized": Message: Not Allowed
        "404 Not Found": Message: Not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
# 12. Expense_accounts
* ### fetch single expense_account for the business
```javascript
        Endpoint: GET /API/accounts/single/{account_id}
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Single account details.
        "401 Unauthorized": Message: Not allowed
        "404 Not Found": Message: Account not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### Fetch all expense accounts for the business* ### activate-account
activate business account for the business
```javascript
    endpoint : GET API/business/activate-account{business_id}
    method : POST
    Content Type: "Application/Json"
    Status Codes:
      "200": success
      " 400": account already activate
      " 404": business not found 
    headers :
      X-API-KEY : <API_KEY>
    body : {
}
```
```javascript
        Endpoint: GET /API/accounts/all
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": All accounts records.

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {}
```
* ### create expense account for the business
```javascript
        Endpoint: POST /API/accounts/create-account
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Account has been created.
        "409 Conflict": Message: This account already exists.

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "accountName": "Account Name",
        "description": "Description"
    }
```
* ### update expense account
```javascript
    Endpoint: PUT /API/accounts/update/{account_id}
    Method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Account Updated.
        "401 Unauthorized": Message: Incorrect password
        "404 Not Found": Message: Account doesn't exist
        "409 Conflict": Message: This account name already exists

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "accountName": "New Account Name",
        "description": "New Description",
        "password": "xxxx"
    }
```
* ### Delete expense_accounts for the business
```javascript
        Endpoint: DELETE /API/accounts/delete/{account_id}
    Method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Message: Account Deleted.
        "401 Unauthorized": Message: Incorrect password
        "404 Not Found": Message: Account Not Found
        "400 Bad Request": Message: Not allowed

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "password": "xxxx"
    }
```
# 13. admin
###  add-categories
```javascript
     endpoint: GET API/admin/add-categories
     method: POST
     content-type: "application/json"
     status codes:
        "200 OK": Message: Category added succesfully
        
     headers:
        x-access-token: <LOGIN_TOKEN>
     body: {
        
     }
```                                             


* ### add service categories
```javascript
     endpoint: GET API/admin/add-service-categories
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "201 Created": Service Categories added successfully

    body: {
        "categories": ["Category1", "Category2", ...]
    }
``` 
# 14. services
* ### fetch all services
 fetch all services

```javascript

     endpoint : GET /API/services/fetch_all
     method : GET
     Status Code : 
       "200 " : Success
     headers : 
       X-API-Key : <API_KEY>
     body : {
}
```