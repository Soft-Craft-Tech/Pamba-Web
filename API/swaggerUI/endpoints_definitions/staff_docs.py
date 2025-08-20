from flasgger import SwaggerView
from API.lib.auth import business_login_required, verify_api_key, business_verification_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

ADD_STAFF = {
    'tags': ['Staff'],
    'summary': 'Create a new staff member',
    'description': 'Allows a logged-in and verified business to create a new staff member',
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
                    'f_name': {'type': 'string', 'description': 'Full name of the staff member', 'example': 'John Doe'},
                    'phone': {'type': 'string', 'description': 'Phone number of the staff member', 'example': '+1234567890'},
                    'role': {'type': 'string', 'description': 'Role of the staff member', 'example': 'Stylist'}
                },
                'required': ['f_name', 'phone', 'role']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Staff created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Staff Created'},
                    'staff': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'f_name': {'type': 'string', 'example': 'John Doe'},
                            'phone': {'type': 'string', 'example': '+1234567890'},
                            'role': {'type': 'string', 'example': 'Stylist'},
                            'public_id': {'type': 'string', 'example': 'a1b2c3d4e5f6'},
                            'employer_id': {'type': 'integer', 'example': 1}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request - Invalid payload or unexpected issue',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Invalid payload: 'f_name' key is required"}
                }
            }
        },
        409: {
            'description': 'Conflict - Phone number already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Phone number already exists'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

DELETE_STAFF = {
    'tags': ['Staff'],
    'summary': 'Delete a staff member',
    'description': 'Allows a logged-in and verified business to delete a staff member by ID',
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
            'name': 'staff_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the staff member to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Staff deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Staff deleted'},
                    'staff': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'f_name': {'type': 'string', 'example': 'John Doe'},
                            'phone': {'type': 'string', 'example': '+1234567890'},
                            'role': {'type': 'string', 'example': 'Stylist'},
                            'public_id': {'type': 'string', 'example': 'a1b2c3d4e5f6'},
                            'employer_id': {'type': 'integer', 'example': 1}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized - Not allowed to delete this staff member',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Not allowed'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

UPDATE_STAFF = {
    'tags': ['Staff'],
    'summary': 'Update staff information',
    'description': 'Allows a logged-in and verified business to update a staff member’s phone and role',
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
            'name': 'staff_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the staff member to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'phone': {'type': 'string', 'description': 'Updated phone number of the staff member', 'example': '+1234567890'},
                    'role': {'type': 'string', 'description': 'Updated role of the staff member', 'example': 'Manager'}
                },
                'required': ['phone', 'role']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Staff updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Updated'},
                    'staff': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'f_name': {'type': 'string', 'example': 'John Doe'},
                            'phone': {'type': 'string', 'example': '+1234567890'},
                            'role': {'type': 'string', 'example': 'Manager'},
                            'public_id': {'type': 'string', 'example': 'a1b2c3d4e5f6'},
                            'employer_id': {'type': 'integer', 'example': 1}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized - Not allowed to update this staff member',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Not allowed'}
                }
            }
        },
        409: {
            'description': 'Conflict - Phone number already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Phone number already exists'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_SINGLE_STAFF = {
    'tags': ['Staff'],
    'summary': 'Fetch a single staff member’s information',
    'description': 'Allows a logged-in business to retrieve details of a specific staff member by ID',
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
            'name': 'staff_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the staff member to fetch'
        }
    ],
    'responses': {
        200: {
            'description': 'Staff information retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'staff': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'f_name': {'type': 'string', 'example': 'John Doe'},
                            'phone': {'type': 'string', 'example': '+1234567890'},
                            'role': {'type': 'string', 'example': 'Stylist'},
                            'public_id': {'type': 'string', 'example': 'a1b2c3d4e5f6'},
                            'employer_id': {'type': 'integer', 'example': 1}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized - Not allowed to access this staff member',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Not Allowed'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_ALL_STAFF = {
    'tags': ['Staff'],
    'summary': 'Fetch all staff for a business',
    'description': 'Retrieves all staff members associated with a business identified by its slug',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'slug',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Unique slug of the business',
            'example': 'example-business'
        }
    ],
    'responses': {
        200: {
            'description': 'Staff list retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'staff': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'f_name': {'type': 'string', 'example': 'John Doe'},
                                'phone': {'type': 'string', 'example': '+1234567890'},
                                'role': {'type': 'string', 'example': 'Stylist'},
                                'public_id': {'type': 'string', 'example': 'a1b2c3d4e5f6'},
                                'employer_id': {'type': 'integer', 'example': 1}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_STAFF_UNAVAILABILITY = {
    'tags': ['Staff'],
    'summary': 'Check staff availability',
    'description': 'Checks if a staff member is available at a specified date and time',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'staff_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the staff member to check availability for'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'date': {'type': 'string', 'description': 'Date to check availability (DD-MM-YYYY)', 'example': '13-08-2025'},
                    'time': {'type': 'string', 'description': 'Time to check availability (HH:MM)', 'example': '14:00'}
                },
                'required': ['date', 'time']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Staff is available at the specified time',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Staff is available'}
                }
            }
        },
        400: {
            'description': 'Bad Request - Staff not available or invalid input',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Staff is booked at this time'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

ADD_STAFF_UNAVAILABILITY = {
    'tags': ['Staff'],
    'summary': 'Add staff unavailability periods',
    'description': 'Allows a logged-in and verified business to add unavailability periods for a staff member, either for the entire day or specific time periods',
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
            'name': 'staff_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the staff member to add unavailability for'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'date': {'type': 'string', 'description': 'Date of unavailability (DD-MM-YYYY)', 'example': '13-08-2025'},
                    'all_day': {'type': 'boolean', 'description': 'Whether the staff is unavailable for the entire day', 'example': False},
                    'periods': {
                        'type': 'array',
                        'description': 'List of unavailability periods (required if all_day is False)',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'startTime': {'type': 'string', 'description': 'Start time of unavailability (HH:MM)', 'example': '09:00'},
                                'endTime': {'type': 'string', 'description': 'End time of unavailability (HH:MM)', 'example': '11:00'}
                            },
                            'required': ['startTime', 'endTime']
                        }
                    }
                },
                'required': ['date', 'all_day']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Unavailability added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Staff unavailability added successfully'}
                }
            }
        },
        400: {
            'description': 'Bad Request - Invalid input or date in the past',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Invalid date format. Use DD-MM-YYYY'}
                }
            }
        },
        401: {
            'description': 'Unauthorized - Not allowed to manage this staff member',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Unauthorized: Not allowed to manage this staff'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

