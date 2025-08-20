from flasgger import SwaggerView
from API.lib.auth import verify_api_key, client_login_required, business_login_required

# Import common responses from existing file
from API.swaggerUI.common_responses import COMMON_RESPONSES

CLIENT_SIGNUP = {
    'tags': ['Clients'],
    'summary': 'Sign up a new client',
    'description': 'Creates a new client account and sends an OTP for verification',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Client email', 'example': 'client@example.com'},
                    'phone': {'type': 'string', 'description': 'Client phone number', 'example': '+254123456789'},
                    'name': {'type': 'string', 'description': 'Client name', 'example': 'John Doe'},
                    'password': {'type': 'string', 'description': 'Client password', 'example': 'securepassword123'}
                },
                'required': ['email', 'phone', 'name', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Client signup successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Signup Success. An OTP has been sent to your email.'},
                    'email': {'type': 'string', 'example': 'client@example.com'},
                    'Client': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'email': {'type': 'string', 'example': 'client@example.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'verified': {'type': 'boolean', 'example': False},
                            'profile_image': {'type': 'string', 'example': None},
                            'dob': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        409: {
            'description': 'Conflict - Email or phone already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Email already exists!'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

VERIFY_CLIENT_OTP = {
    'tags': ['Clients'],
    'summary': 'Verify client account with OTP',
    'description': 'Verifies a client’s account using the OTP sent during signup',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Client email', 'example': 'client@example.com'},
                    'otp': {'type': 'string', 'description': 'One-time password', 'example': '123456'}
                },
                'required': ['email', 'otp']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Account verified successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Account activated'},
                    'client': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'email': {'type': 'string', 'example': 'client@example.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'verified': {'type': 'boolean', 'example': True},
                            'profile_image': {'type': 'string', 'example': None},
                            'dob': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

REQUEST_ACCOUNT_DELETION = {
    'tags': ['Clients'],
    'summary': 'Request client account deletion',
    'description': 'Allows a client to request deletion of their personal data, with a 30-day grace period',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Client email', 'example': 'client@example.com'},
                    'reason': {'type': 'string', 'description': 'Reason for deletion', 'example': 'No longer using the service'}
                },
                'required': ['email', 'reason']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Deletion request submitted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'We are sorry to see you leave. Your data will be deleted in 30 days'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

CLIENT_LOGIN = {
    'tags': ['Clients'],
    'summary': 'Client login',
    'description': 'Authenticates a client using email and password, returning a JWT token',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Basic Auth with email:password'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Login Successful'},
                    'client': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'email': {'type': 'string', 'example': 'client@example.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'verified': {'type': 'boolean', 'example': True},
                            'profile_image': {'type': 'string', 'example': None},
                            'dob': {'type': 'string', 'example': None}
                        }
                    },
                    'authToken': {'type': 'string', 'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

REQUEST_PASSWORD_RESET = {
    'tags': ['Clients'],
    'summary': 'Request password reset',
    'description': 'Sends a password reset token to the client’s email, valid for 30 minutes',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Client email', 'example': 'client@example.com'}
                },
                'required': ['email']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Password reset token sent',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Token sent to your email'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RESET_PASSWORD = {
    'tags': ['Clients'],
    'summary': 'Reset client password',
    'description': 'Resets the client’s password using a valid JWT token',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'token',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'JWT token sent for password reset'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'password': {'type': 'string', 'description': 'New password', 'example': 'newpassword123'}
                },
                'required': ['password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Password reset successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Reset Successful'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

CHANGE_PASSWORD = {
    'tags': ['Clients'],
    'summary': 'Change client password',
    'description': 'Allows a logged-in client to change their password',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated client'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'oldPassword': {'type': 'string', 'description': 'Current password', 'example': 'oldpassword123'},
                    'newPassword': {'type': 'string', 'description': 'New password', 'example': 'newpassword123'}
                },
                'required': ['oldPassword', 'newPassword']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Password changed successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Password changed'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

UPDATE_PROFILE = {
    'tags': ['Clients'],
    'summary': 'Update client profile',
    'description': 'Allows a logged-in client to update their profile, including email, phone, date of birth, and profile image',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated client'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'payload',
            'in': 'formData',
            'type': 'string',
            'description': 'JSON string containing email, phone, and dob',
            'example': '{"email": "client@example.com", "phone": "+254123456789", "dob": "01-01-1990"}'
        },
        {
            'name': 'image',
            'in': 'formData',
            'type': 'file',
            'description': 'Profile image file'
        }
    ],
    'consumes': ['multipart/form-data'],
    'responses': {
        200: {
            'description': 'Profile updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Update Successful'},
                    'client': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'email': {'type': 'string', 'example': 'client@example.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'verified': {'type': 'boolean', 'example': True},
                            'profile_image': {'type': 'string', 'example': 'profile_image.jpg'},
                            'dob': {'type': 'string', 'example': '1990-01-01'}
                        }
                    }
                }
            }
        },
        409: {
            'description': 'Conflict - Email or phone already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Email already exists'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RESEND_VERIFICATION_OTP = {
    'tags': ['Clients'],
    'summary': 'Resend verification OTP',
    'description': 'Resends a verification OTP to a client who hasn’t verified their account',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Client email', 'example': 'client@example.com'}
                },
                'required': ['email']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'OTP sent successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'OTP sent to: cli*****@example.com'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_BUSINESS_CLIENTS = {
    'tags': ['Clients'],
    'summary': 'Fetch clients associated with a business',
    'description': 'Retrieves all clients who have booked appointments with a logged-in business, along with analytics',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated business'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        }
    ],
    'responses': {
        200: {
            'description': 'Clients retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'lifetime_client_number_of_clients': {'type': 'integer', 'example': 10},
                    'all_clients': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'name': {'type': 'string', 'example': 'John Doe'},
                                'email': {'type': 'string', 'example': 'client@example.com'},
                                'phone': {'type': 'string', 'example': '+254123456789'},
                                'verified': {'type': 'boolean', 'example': True},
                                'profile_image': {'type': 'string', 'example': None},
                                'dob': {'type': 'string', 'example': None}
                            }
                        }
                    },
                    'all_appointments': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Jan': {'type': 'integer', 'example': 5},
                                'Feb': {'type': 'integer', 'example': 3}
                            }
                        }
                    },
                    'returning_clients': {'type': 'integer', 'example': 2}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RETRIEVE_CLIENT = {
    'tags': ['Clients'],
    'summary': 'Retrieve client profile',
    'description': 'Fetches the profile details of the logged-in client',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated client'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        }
    ],
    'responses': {
        200: {
            'description': 'Client profile retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'client': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'email': {'type': 'string', 'example': 'client@example.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'verified': {'type': 'boolean', 'example': True},
                            'profile_image': {'type': 'string', 'example': 'profile_image.jpg'},
                            'dob': {'type': 'string', 'example': '1990-01-01'}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

