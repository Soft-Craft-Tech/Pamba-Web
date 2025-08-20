# TODO : Refactor out the re-occuring part for reusability. Like the responses. Or create a factory functions.
from flasgger import SwaggerView
from API.lib.auth import verify_api_key, business_login_required, business_verification_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

def route_docs_generator():
    """
        Configure the swagger documentation for each route.

    """


ACCOUNT_ACTIVATION = {
    'tags': ['Business Account'],
    'summary': 'Activate business account',
    'description': 'Activate a business account using a verification token',
    'parameters': [
        {
            'name': 'token',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Account activation token'
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
            'description': 'Account activated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Success'
                    },
                    'username': {
                        'type': 'string',
                        'example': 'business-slug'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - Invalid token or account already active',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'examples': ['Token Invalid or Expired', 'Account already active']
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized - Invalid API key',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Invalid API key'
                    }
                }
            }
        },
        404: {
            'description': 'Business not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Not Found'
                    }
                }
            }
        }
    }
}


BUSINESS_SIGNUP = {
    'tags': ['Business Account'],
    'summary': 'Register a new business account',
    'description': 'Create a new business account and send an activation email',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'Business name', 'example': 'Pamba Salon'},
                    'email': {'type': 'string', 'description': 'Business email', 'example': 'contact@pamba.com'},
                    'phone': {'type': 'string', 'description': 'Business phone number', 'example': '+254123456789'},
                    'city': {'type': 'string', 'description': 'City where business is located', 'example': 'Nairobi'},
                    'category': {'type': 'string', 'description': 'Business category ID or name', 'example': '1'},
                    'password': {'type': 'string', 'description': 'Business account password', 'example': 'securepassword123'},
                    'location': {
                        'type': 'object',
                        'properties': {
                            'place_id': {'type': 'string', 'description': 'Google Maps place ID', 'example': 'ChIJ...'},
                            'formatted_address': {'type': 'string', 'description': 'Full address', 'example': '123 Main St, Nairobi'},
                            'geometry': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'object',
                                        'properties': {
                                            'lat': {'type': 'number', 'description': 'Latitude', 'example': -1.292066},
                                            'lng': {'type': 'number', 'description': 'Longitude', 'example': 36.821946}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'required': ['name', 'email', 'phone', 'city', 'category', 'password', 'location']
            }
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
        201: {
            'description': 'Business account created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Successful! Account activation link set to your email'},
                    'business': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'business_name': {'type': 'string', 'example': 'Pamba Salon'},
                            'slug': {'type': 'string', 'example': 'pamba-salon'},
                            'email': {'type': 'string', 'example': 'contact@pamba.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'city': {'type': 'string', 'example': 'Nairobi'},
                            'formatted_address': {'type': 'string', 'example': '123 Main St, Nairobi'},
                            'latitude': {'type': 'number', 'example': -1.292066},
                            'longitude': {'type': 'number', 'example': 36.821946},
                            'category_id': {'type': 'integer', 'example': 1}
                        }
                    },
                    'activationToken': {'type': 'string', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RESEND_VERIFICATION_TOKEN = {
    'tags': ['Business Account'],
    'summary': 'Resend business account activation token',
    'description': 'Resend an account activation token to the business email',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Business email', 'example': 'contact@pamba.com'}
                },
                'required': ['email']
            }
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
            'description': 'Activation email sent successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Account verification email has been sent to your inbox'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

CHECK_TOKEN_EXPIRY = {
    'tags': ['Business Account'],
    'summary': 'Check if a token is expired',
    'description': 'Verify if a provided token is still valid or has expired',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string', 'description': 'Token to check', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
                },
                'required': ['token']
            }
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
            'description': 'Token expiry status',
            'schema': {
                'type': 'object',
                'properties': {
                    'expired': {'type': 'boolean', 'example': False}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

LOGIN = {
    'tags': ['Business Account'],
    'summary': 'Business login',
    'description': 'Authenticate a business user and return an auth token',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Basic Auth credentials (username:password)',
            'example': 'Basic contact:pamba.com:securepassword123'
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
                            'business_name': {'type': 'string', 'example': 'Pamba Salon'},
                            'slug': {'type': 'string', 'example': 'pamba-salon'},
                            'email': {'type': 'string', 'example': 'contact@pamba.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'city': {'type': 'string', 'example': 'Nairobi'},
                            'formatted_address': {'type': 'string', 'example': '123 Main St, Nairobi'},
                            'latitude': {'type': 'number', 'example': -1.292066},
                            'longitude': {'type': 'number', 'example': 36.821946},
                            'category_id': {'type': 'integer', 'example': 1}
                        }
                    },
                    'authToken': {'type': 'string', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

REQUEST_PASSWORD_RESET = {
    'tags': ['Business Account'],
    'summary': 'Request password reset',
    'description': 'Send a password reset link to the business email',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'description': 'Business email', 'example': 'contact@pamba.com'}
                },
                'required': ['email']
            }
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
            'description': 'Password reset email sent',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Reset link has been sent to your email'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RESET_PASSWORD = {
    'tags': ['Business Account'],
    'summary': 'Reset business password',
    'description': 'Reset the business password using a reset token',
    'parameters': [
        {
            'name': 'reset_token',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Password reset token'
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
            'description': 'Password reset successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Password Reset Successful'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RESEND_ACTIVATION_EMAIL = {
    'tags': ['Business Account'],
    'summary': 'Resend activation email for logged-in business',
    'description': 'Resend account activation email for a logged-in, unverified business',
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
            'description': 'Activation email resent successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Account verification email has been sent to your inbox'},
                    'activationToken': {'type': 'string', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

UPDATE_PROFILE = {
    'tags': ['Business Profile'],
    'summary': 'Update business profile',
    'description': 'Update the profile details of a logged-in business',
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
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'Business name', 'example': 'Pamba Salon'},
                    'email': {'type': 'string', 'description': 'Business email', 'example': 'contact@pamba.com'},
                    'phone': {'type': 'string', 'description': 'Business phone number', 'example': '+254123456789'},
                    'city': {'type': 'string', 'description': 'City', 'example': 'Nairobi'},
                    'description': {'type': 'string', 'description': 'Business description', 'example': 'A premium salon service'},
                    'password': {'type': 'string', 'description': 'Current password for verification', 'example': 'securepassword123'},
                    'location': {
                        'type': 'object',
                        'properties': {
                            'place_id': {'type': 'string', 'description': 'Google Maps place ID', 'example': 'ChIJ...'},
                            'formatted_address': {'type': 'string', 'description': 'Full address', 'example': '123 Main St, Nairobi'},
                            'geometry': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'object',
                                        'properties': {
                                            'lat': {'type': 'number', 'description': 'Latitude', 'example': -1.292066},
                                            'lng': {'type': 'number', 'description': 'Longitude', 'example': 36.821946}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'required': ['name', 'email', 'phone', 'city', 'password', 'location']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Profile updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Update Successful'},
                    'business': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'business_name': {'type': 'string', 'example': 'Pamba Salon'},
                            'slug': {'type': 'string', 'example': 'pamba-salon'},
                            'email': {'type': 'string', 'example': 'contact@pamba.com'},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'city': {'type': 'string', 'example': 'Nairobi'},
                            'formatted_address': {'type': 'string', 'example': '123 Main St, Nairobi'},
                            'latitude': {'type': 'number', 'example': -1.292066},
                            'longitude': {'type': 'number', 'example': 36.821946},
                            'description': {'type': 'string', 'example': 'A premium salon service'}
                        }
                    },
                    'authToken': {'type': 'string', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

CHANGE_PASSWORD = {
    'tags': ['Business Account'],
    'summary': 'Change business password',
    'description': 'Change the password for a logged-in business',
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
                    'message': {'type': 'string', 'example': 'Success! Password has been changed'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

ASSIGN_SERVICES = {
    'tags': ['Business Services'],
    'summary': 'Assign services to a business',
    'description': 'Add services offered by a logged-in and verified business',
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
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'services': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string', 'description': 'Service name', 'example': 'Haircut'},
                                'price': {'type': 'number', 'description': 'Service price', 'example': 500},
                                'description': {'type': 'string', 'description': 'Service description', 'example': 'Standard haircut'},
                                'estimatedTime': {'type': 'number', 'description': 'Estimated service time in minutes', 'example': 30},
                                'category': {'type': 'string', 'description': 'Service category', 'example': 'Hair Services'}
                            },
                            'required': ['name', 'price', 'description', 'estimatedTime', 'category']
                        }
                    }
                },
                'required': ['services']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Services added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Services have been Added'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

REMOVE_SERVICE = {
    'tags': ['Business Services'],
    'summary': 'Remove a service from a business',
    'description': 'Remove a specific service offered by a logged-in and verified business',
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
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'serviceId': {'type': 'integer', 'description': 'ID of the service to remove', 'example': 1}
                },
                'required': ['serviceId']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Service removed successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Service removed'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_ALL_BUSINESSES = {
    'tags': ['Businesses'],
    'summary': 'Fetch all active businesses',
    'description': 'Retrieve a list of all active and verified businesses with completed profiles',
    'parameters': [
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
            'description': 'Businesses retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'businesses': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'business_name': {'type': 'string', 'example': 'Pamba Salon'},
                                'slug': {'type': 'string', 'example': 'pamba-salon'},
                                'email': {'type': 'string', 'example': 'contact@pamba.com'},
                                'phone': {'type': 'string', 'example': '+254123456789'},
                                'city': {'type': 'string', 'example': 'Nairobi'},
                                'formatted_address': {'type': 'string', 'example': '123 Main St, Nairobi'},
                                'latitude': {'type': 'number', 'example': -1.292066},
                                'longitude': {'type': 'number', 'example': 36.821946},
                                'reviews': {'type': 'integer', 'example': 5}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_BUSINESS = {
    'tags': ['Businesses'],
    'summary': 'Fetch a specific business by slug',
    'description': 'Retrieve details of a specific business by its slug, including services, ratings, and reviews',
    'parameters': [
        {
            'name': 'slug',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Business slug'
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
            'description': 'Business details retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'business': {
                        'type': 'object',
                        'properties': {
                            'business_name': {'type': 'string', 'example': 'Pamba Salon'},
                            'category': {'type': 'string', 'example': 'Salon'},
                            'id': {'type': 'integer', 'example': 1},
                            'phone': {'type': 'string', 'example': '+254123456789'},
                            'description': {'type': 'string', 'example': 'A premium salon service'},
                            'imageUrl': {'type': 'string', 'example': 'https://example.com/image.jpg'},
                            'city': {'type': 'string', 'example': 'Nairobi'},
                            'email': {'type': 'string', 'example': 'contact@pamba.com'},
                            'rating': {'type': 'number', 'example': 4.5},
                            'latitude': {'type': 'number', 'example': -1.292066},
                            'longitude': {'type': 'number', 'example': 36.821946},
                            'formatted_address': {'type': 'string', 'example': '123 Main St, Nairobi'},
                            'placeId': {'type': 'string', 'example': 'ChIJ...'},
                            'profile_completed': {'type': 'boolean', 'example': True}
                        }
                    },
                    'services': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'service': {'type': 'string', 'example': 'Haircut'},
                                'price': {'type': 'number', 'example': 500},
                                'description': {'type': 'string', 'example': 'Standard haircut'},
                                'estimated_service_time': {'type': 'number', 'example': 30}
                            }
                        }
                    },
                    'ratingsAverage': {'type': 'number', 'example': 4.5},
                    'ratingsBreakdown': {
                        'type': 'object',
                        'example': {'1': 0, '2': 1, '3': 2, '4': 5, '5': 10}
                    },
                    'reviews': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'comment': {'type': 'string', 'example': 'Great service!'},
                                'created_at': {'type': 'string', 'example': '2025-08-12T17:29:51Z'}
                            }
                        }
                    },
                    'gallery': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

GET_BUSINESS_ANALYTICS = {
    'tags': ['Business Analytics'],
    'summary': 'Fetch business analytics',
    'description': 'Retrieve analytics data for a logged-in and verified business, including appointments, revenue, and expenses',
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
            'description': 'Analytics data retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'all_appointments': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'date': {'type': 'string', 'example': '2025-08-12'},
                                'completed': {'type': 'boolean', 'example': False}
                            }
                        }
                    },
                    'today_appointments': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'date': {'type': 'string', 'example': '2025-08-12'},
                                'service': {'type': 'string', 'example': 'Haircut'}
                            }
                        }
                    },
                    'today_revenue': {'type': 'number', 'example': 500},
                    'current_month_revenue': {'type': 'number', 'example': 15000},
                    'lifetime_sales': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'price': {'type': 'number', 'example': 500},
                                'date_created': {'type': 'string', 'example': '2025-08-12T17:29:51Z'}
                            }
                        }
                    },
                    'current_month_expenses': {'type': 'number', 'example': 2000},
                    'lifetime_expenses': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'amount': {'type': 'number', 'example': 1000},
                                'created_at': {'type': 'string', 'example': '2025-08-12T17:29:51Z'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

SERVICE_BUSINESSES = {
    'tags': ['Businesses'],
    'summary': 'Fetch businesses by service',
    'description': 'Retrieve businesses offering a specific service',
    'parameters': [
        {
            'name': 'service_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the service'
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
            'description': 'Businesses retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'businesses': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string', 'example': 'Pamba Salon'},
                                'categories': {'type': 'string', 'example': 'Salon'},
                                'city': {'type': 'string', 'example': 'Nairobi'},
                                'id': {'type': 'integer', 'example': 1},
                                'phone': {'type': 'string', 'example': '+254123456789'},
                                'ratingsAverage': {'type': 'number', 'example': 4.5},
                                'latitude': {'type': 'number', 'example': -1.292066},
                                'longitude': {'type': 'number', 'example': 36.821946},
                                'place_id': {'type': 'string', 'example': 'ChIJ...'},
                                'formatted_address': {'type': 'string', 'example': '123 Main St, Nairobi'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

UPLOAD_PROFILE_IMG = {
    'tags': ['Business Profile'],
    'summary': 'Upload business profile image',
    'description': 'Upload a profile image for a logged-in and verified business',
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
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'imageURL': {'type': 'string', 'description': 'URL of the profile image', 'example': 'https://example.com/image.jpg'}
                },
                'required': ['imageURL']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Profile image uploaded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

UPDATE_DESCRIPTION = {
    'tags': ['Business Profile'],
    'summary': 'Update business description',
    'description': 'Update the description for a logged-in and verified business',
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
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string', 'description': 'Business description', 'example': 'A premium salon service'}
                },
                'required': ['description']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Description updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Update Successful'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

PROFILE_COMPLETION_STATUS = {
    'tags': ['Business Profile'],
    'summary': 'Check business profile completion status',
    'description': 'Retrieve the completion status of a logged-in business profile',
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
            'description': 'Profile completion status retrieved',
            'schema': {
                'type': 'object',
                'properties': {
                    'profileImg': {'type': 'boolean', 'example': True},
                    'description': {'type': 'boolean', 'example': True},
                    'services': {'type': 'boolean', 'example': True},
                    'expenseAccounts': {'type': 'boolean', 'example': False},
                    'openingAndClosing': {'type': 'boolean', 'example': True}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_BUSINESS_CATEGORIES = {
    'tags': ['Business Categories'],
    'summary': 'Fetch all business categories',
    'description': 'Retrieve a list of all business categories',
    'parameters': [
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
            'description': 'Business categories retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Successful'},
                    'categories': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'category_name': {'type': 'string', 'example': 'Salon'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

ADD_BUSINESS_HOURS = {
    'tags': ['Business Profile'],
    'summary': 'Add business operating hours',
    'description': 'Set the operating hours for a logged-in and verified business',
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
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'weekdayOpening': {'type': 'string', 'description': 'Weekday opening time (HH:MM)', 'example': '09:00'},
                    'weekdayClosing': {'type': 'string', 'description': 'Weekday closing time (HH:MM)', 'example': '17:00'},
                    'weekendOpening': {'type': 'string', 'description': 'Weekend opening time (HH:MM)', 'example': '10:00'},
                    'weekendClosing': {'type': 'string', 'description': 'Weekend closing time (HH:MM)', 'example': '16:00'}
                },
                'required': ['weekdayOpening', 'weekdayClosing', 'weekendOpening', 'weekendClosing']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Business hours added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Successful! Business hours added'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_BUSINESS_SERVICES = {
    'tags': ['Business Services'],
    'summary': 'Fetch services of a business',
    'description': 'Retrieve all services offered by a specific business identified by its slug',
    'parameters': [
        {
            'name': 'slug',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Business slug'
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
            'description': 'Services retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'services': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'service': {'type': 'string', 'example': 'Haircut'},
                                'price': {'type': 'number', 'example': 500},
                                'description': {'type': 'string', 'example': 'Standard haircut'},
                                'estimated_service_time': {'type': 'number', 'example': 30},
                                'category_name': {'type': 'string', 'example': 'Hair Services'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

SEARCH_BUSINESSES_BY_LOCATION_AND_SERVICE = {
    'tags': ['Businesses'],
    'summary': 'Search businesses by location and service',
    'description': 'Search for businesses offering a specific service within a certain location',
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
                    'service': {'type': 'string', 'description': 'Service name', 'example': 'Haircut'},
                    'latitude': {'type': 'number', 'description': 'Latitude of search location', 'example': -1.292066},
                    'longitude': {'type': 'number', 'description': 'Longitude of search location', 'example': 36.821946}
                },
                'required': ['service', 'latitude', 'longitude']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Businesses retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'businesses': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'name': {'type': 'string', 'example': 'Pamba Salon'},
                                'latitude': {'type': 'number', 'example': -1.292066},
                                'longitude': {'type': 'number', 'example': 36.821946},
                                'reviews': {'type': 'integer', 'example': 5}
                            }
                        }
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'An error occurred'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

