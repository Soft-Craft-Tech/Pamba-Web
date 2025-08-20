from flasgger import SwaggerView
from API.lib.auth import verify_api_key, business_login_required, business_verification_required

# Import common responses from existing file
from API.swaggerUI.common_responses import COMMON_RESPONSES

FETCH_SERVICE_CATEGORIES = {
    'tags': ['Services'],
    'summary': 'Fetch all service categories',
    'description': 'Retrieves a list of all service categories ordered by category name',
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
            'description': 'Service categories retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'categories': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'category': {'type': 'string', 'example': 'Haircut'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_ALL_SERVICES = {
    'tags': ['Services'],
    'summary': 'Fetch all services',
    'description': 'Retrieves all services from active, verified, and profile-completed businesses, including business details',
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
            'description': 'Services retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'services': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'serviceInfo': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer', 'example': 1},
                                        'service': {'type': 'string', 'example': 'Haircut'},
                                        'description': {'type': 'string', 'example': 'Standard haircut service'},
                                        'price': {'type': 'number', 'example': 20.0},
                                        'estimated_service_time': {'type': 'number', 'example': 1.5},
                                        'business_id': {'type': 'integer', 'example': 1},
                                        'service_category': {'type': 'integer', 'example': 1}
                                    }
                                },
                                'businessInfo': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer', 'example': 1},
                                        'business_name': {'type': 'string', 'example': 'Example Salon'},
                                        'slug': {'type': 'string', 'example': 'example-salon'},
                                        'phone': {'type': 'string', 'example': '+1234567890'},
                                        'formatted_address': {'type': 'string', 'example': '123 Main St, City, Country'},
                                        'latitude': {'type': 'number', 'example': 40.7128},
                                        'longitude': {'type': 'number', 'example': -74.0060},
                                        'place_id': {'type': 'string', 'example': 'ChIJN1t_tDeuEmsRUsoyG83frY4'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RETRIEVE_SERVICE = {
    'tags': ['Services'],
    'summary': 'Retrieve a single service',
    'description': 'Fetches details of a specific service by ID, including business details and staff information',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'service_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the service to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Service retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'service': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'service': {'type': 'string', 'example': 'Haircut'},
                            'description': {'type': 'string', 'example': 'Standard haircut service'},
                            'price': {'type': 'number', 'example': 20.0},
                            'business_id': {'type': 'integer', 'example': 1},
                            'service_category': {'type': 'integer', 'example': 1},
                            'estimated_time_string': {'type': 'string', 'example': '1 Hour(s), 30 minutes'},
                            'business_name': {'type': 'string', 'example': 'Example Salon'},
                            'weekdayOpening': {'type': 'string', 'example': '09:00'},
                            'weekdayClosing': {'type': 'string', 'example': '17:00'},
                            'weekendOpening': {'type': 'string', 'example': '10:00'},
                            'weekendClosing': {'type': 'string', 'example': '16:00'},
                            'slug': {'type': 'string', 'example': 'example-salon'},
                            'phone': {'type': 'string', 'example': '+1234567890'},
                            'formatted_address': {'type': 'string', 'example': '123 Main St, City, Country'},
                            'latitude': {'type': 'number', 'example': 40.7128},
                            'longitude': {'type': 'number', 'example': -74.0060},
                            'place_id': {'type': 'string', 'example': 'ChIJN1t_tDeuEmsRUsoyG83frY4'},
                            'directions': {'type': 'string', 'example': 'https://www.google.com/maps/search/?api=1&query=40.7128,-74.0060&query_place_id=ChIJN1t_tDeuEmsRUsoyG83frY4'}
                        }
                    },
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

UPDATE_SERVICE = {
    'tags': ['Services'],
    'summary': 'Update a service',
    'description': 'Allows a logged-in and verified business to update a service’s details (name, price, description, estimated time, or category)',
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
            'name': 'service_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the service to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'Updated name of the service', 'example': 'Premium Haircut'},
                    'price': {'type': 'number', 'description': 'Updated price of the service', 'example': 25.0},
                    'description': {'type': 'string', 'description': 'Updated description of the service', 'example': 'Premium haircut with styling'},
                    'estimatedTime': {'type': 'number', 'description': 'Updated estimated service time in hours', 'example': 1.75},
                    'category': {'type': 'integer', 'description': 'Updated service category ID', 'example': 2}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Service updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Service Update successfully'},
                    'service': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'service': {'type': 'string', 'example': 'Premium Haircut'},
                            'description': {'type': 'string', 'example': 'Premium haircut with styling'},
                            'price': {'type': 'number', 'example': 25.0},
                            'estimated_service_time': {'type': 'number', 'example': 1.75},
                            'business_id': {'type': 'integer', 'example': 1},
                            'service_category': {'type': 'integer', 'example': 2}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to update this service',
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

DELETE_SERVICE = {
    'tags': ['Services'],
    'summary': 'Delete a service',
    'description': 'Allows a logged-in and verified business to delete a specific service by ID',
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
            'name': 'service_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the service to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Service deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Service Deleted successfully'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this service',
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
