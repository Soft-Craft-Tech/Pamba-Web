# Pamba Endpoint Docs

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

* ### Client Verification with OTP after signup
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

# clients
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
* ### Delete Account
### Client delete account 
```javascript
     endpoint: POST API/clients/delete-account
     method: POST
     Content-Type: Application/Json
     Status Codes:
       "200 OK": Message "We are sorry to see you leave. Your data will be deleted in 30 days"
       "400 ": Message  "Deletion request will be done on  number of days remaining"
       "400" : Message "Email doesn't exist"
```
* ### Fetch all clients associated with a certain business
```javascript
     Endpoint: GET /API/clients/business-clients
     Method: GET
     Content Type: "Application/Json"

     Status Codes: 
    "200 OK": All clients associated with the logged-in business fetched successfully.
    "401 Unauthorized": Not authorized to access this resource.

    Headers:
    X-API-KEY: <API_KEY>
    x-access-token: <LOGIN_TOKEN>
    Body: {
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
         "oldPassword": "*********",
         "newPassword":"********************************"
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
       "409" : Phone/email number already exists
    
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
         "password": "********"
}
```
# 
* ### assign services
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

     endpoint : GET /businessess/analysis
     method : GET
     Status Code : 
       "200 " : Analysis data
     headers : 
       X-API-Key : <API_KEY>
       x-access-token : <LOGIN-TOKEN>
     body : {
}
```
* ### Fetch Single Business
Fetch a single business given Business id

```javascript
    endpoint: GET /API/businesses/{slug}
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Success, business, services
        "400 Bad Request": Business not verified
        "404 Not Found": Business Not found

    headers:
        X-API-KEY: <API_KEY>
        

    body: {
        
    }
```

* ### Fetch Service Businesses
Fetch Businesses associated with a certain service

```javascript
    endpoint: GET /API/businesses/service-businesses/{slug}
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



# 4. Client Notifications

* ### Read Notification
## Mark notification as read

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
* ### Create notifications for clients.
```javascript
    Endpoint: POST /API/notifications/client/add
    Method: POST
    Content Type: "Application/Json"

    Status Codes: 
       "201 Created": Notification successfully created.
       "401 Unauthorized": Not authorized to access this resource.

    Headers:
    X-API-KEY: <API_KEY>
    x-access-token: <LOGIN_TOKEN>

    Body: 
    {
        "title": <title>,
        "message": <message>,
        "clientID": <client_id>
    }

```
* ### Delete notifications
```javascript
    Endpoint: DELETE /API/notifications/client/delete/<int:notification_id>
Method: DELETE
Content Type: "Application/Json"

Status Codes: 
    "200 OK": Notification successfully deleted.
    "400 Bad Request": Notification not found.
    "401 Unauthorized": Not authorized to access this resource.

Headers:
    X-API-KEY: <API_KEY>
    x-access-token: <LOGIN_TOKEN>


Body: {
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
        "401 Unauthorized": please verify account.
        "404 Not Found": The shop/business/services not found .

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "date": "***",
        "time": "***",
        "comment": "***",
        "provider": "***"
    }
```
 # Book appointment from the web 
```javascript
     endpoint : POST /API/appointments/book/web-appoinments
     method : POST 
     Content Type  : Application/Json
     
     Status Codes: 
      "201 Ok" : Appointment Booked Successfully
      "400" : message "Can't book an appointment on a past date/time"
      " 400" : Message "Our premises are not open at the picked time and date"
      "400" : message  "The Staff you selected is already booked at this time please book with a different staff or let us assign you someone"
      "404" : Service/business not found
      "404" : message "staff you booked with doesnt exist"
      "404" : message "service you are booking is unavailable"
      ""
     headers:
        X-API-KEY: <API_KEY>
    body: {
        "date": "***",         
        "time": "***",         
        "comment": "***",      
        "business": *** ,     
        "staff": *** ,         
        "email": "***",        
        "phone": "***", 
        "name" : "***",        
        "notification": "***"
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
### assign-appointment
```javascript
    endpoint: PUT /API/appointments/assign-appointment/<int:appointment_id>
    method: PUT
    Content Type: "Application/Json"

    Status Codes: 
    "200 OK": Appointment successfully assigned.
    "400 Bad Request":  appointment already cancelled.
    "401 Unauthorized": Incorrect password provided.
    "403 Forbidden": Not allowed to perform action.
    "404 Not Found": Appointment or staff not found.

    headers:
    X-API-KEY: <API_KEY>
    x-access-token: <LOGIN_TOKEN>

    body: 
    {
        "staffID": <****>,
        "password": <******>
    }


```
### Fetch all appointments booked with the logged-in business
```javascript
      endpoint: GET /API/appointments/business-appointments
      method: GET
      Content Type: "Application/Json"

      Status Codes: 
       "200 OK": List of appointments booked with the logged-in business.
       "401 Unauthorized": Not authorized to access this resource.

headers:
    X-API-KEY: <API_KEY>
    x-access-token: <LOGIN_TOKEN>

```
# Fetch Single Appointment
Fetch details of a single appointment.

```javascript

    endpoint: GET API/appointments/{appointment_id}
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Appointment fetched successfully.
        "404 Not Found": Appointment does not exist.

    headers: {}
    body: {}
```
# End Appointment
End an appointment when completed and trigger a notification for an appointment review.

```javascript

    endpoint: PUT API/appointments/end_appointment/{appointment_id}
    method: PUT
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Appointment Ended Successfully.
        "400 Bad Request": Appointment already completed or cannot end a future appointment.
        "401 Unauthorized": Not allowed.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {}
```

# Send Appointment Reminder
Send reminders for upcoming appointments. Reminders can be sent via SMS or WhatsApp.

```javascript

    endpoint: POST API/appointments/send-reminders
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Reminders sent successfully.

    headers:
        X-API-KEY: <API_KEY>
    body: {}
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
        "400 Bad Request": message: Not Allowed 
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
        "200 Created": Message, Updated 
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
      Endpoint: POST /API/reviews/create{appointment_id}
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

### fetch a single sale
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
* ### Business Revenue Analysis 
```javascript
     Endpoint: GET /API/sales/analysis
     Method: GET
     Content Type: "Application/Json"    

     Status Codes: 
       "200 OK": Business revenue analysis successfully retrieved.
       "401 Unauthorized": Not authorized to access this resource.

     Headers:
      X-API-KEY: <API_KEY>
      x-access-token: <LOGIN_TOKEN>
     Body : {
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
        
    }
```
* ### Edit a Sale

```javascript
      Endpoint: PUT /API/sales/edit/{sale_id}
      Method: PUT
      Content Type: "Application/Json"

      Status Codes: 
        "200 OK": Message: Sale updated, Updated Sale.
        "400 Bad Request": Message: Not found or We are not offering this service at the moment.
        "404 Not Found": Message: Sale not found

    Headers:
        x-access-token: <LOGIN_TOKEN>
    Body: {
        "paymentmethod": "New Payment Method",
        "description": "New Description",
        "service_id": <int>
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
* ### fetch all expense_accounts for the business
```javascript
        Endpoint: GET /API/accounts/single/{account_id}
    Method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK":  account details.
        "401 Unauthorized": Message: Not allowed
        "404 Not Found": Message: business  not found

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
# 14. services
* ### fetch all services
 fetch all services

```javascript

     endpoint : GET /API/services/all
     method : GET
     Content-Type : Application/Json
     Status Code : 
       "200 " : Success
     headers : 
       X-API-Key : <API_KEY>
     body : {
}
```
### fetch all service categories
all service categories
```javascript
     endpoint : GET API/services/categories
     method: GET
     Content-Type : Application/Json
     Status Code : 
       "200 " : Success
     headers :
       X-API-Key: <API_KEY>
     body : {

        }
     
```
* #  Retrieve single service.
```javascript
     endpoint : GET API/services/retrieve/{service_id}    
     method : GET
     Content-Type : Application/Json
     Status Code : 
       "200 " : Success  
       "404" : Not Found   
     headers :
       X-API-Key: <API_KEY>
     body : {

        }
   
```

# 15. gallery
* # Fetch Business Gallery
Fetch the business's gallery images.

```javascript

    endpoint: GET API/gallery/{slug}
    method: GET
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Gallery fetched successfully.
        "404 Not Found": Business does not exist.

    headers:
        X-API-KEY: <API_KEY>
    body: {}
```
* ### Add Gallery Image

Add an image to the business's gallery.

```javascript

    endpoint: POST API/gallery/add
    method: POST
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Image added successfully.
        "401 Unauthorized": Not allowed.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {
        "imgURL": "***"  // URL of the image to be added
    }
```
* ### Delete Gallery Image

Delete an image from the business's gallery.

```javascript

    endpoint: GET API/gallery/delete/{image_id}
    method: DELETE
    Content Type: "Application/Json"

    Status Codes: 
        "200 OK": Image deleted successfully.
        "400 Bad Request": Not allowed.
        "404 Not Found": Image does not exist.

    headers:
        X-API-KEY: <API_KEY>
        x-access-token: <LOGIN_TOKEN>
    body: {}
```
* 16. ### messaging
whatsapp notifications
```javascript
     endpoint: GET API/messaging/whatsapp-response
     methods: ["GET","POST"]
     Content-Type: Application/Json
     Status Codes :
        "200" : message " Thank you for contacting Pamba Africa Our staff will respond to you shortly 😊" 
     body: {}
     

```
