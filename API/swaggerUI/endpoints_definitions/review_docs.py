from flasgger import SwaggerView
from API.lib.auth import verify_api_key
from API.swaggerUI.common_responses import COMMON_RESPONSES

CREATE_REVIEW = {
    'tags': ['Reviews'],
    'summary': 'Create a review for a business',
    'description': 'Allows a client to post a review for a business based on an appointment',
    'parameters': [
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'appointment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the appointment being reviewed'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'description': 'Review message', 'example': 'Great service, highly recommend!'}
                },
                'required': ['message']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Review posted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Review has been posted'}
                }
            }
        },
        400: {
            'description': 'Bad Request - Invalid payload',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Invalid payload: 'message' key is required"}
                }
            }
        },
        404: {
            'description': 'Not Found - Appointment does not exist',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Appointment doesn't exist"}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

LIST_REVIEWS = {
    'tags': ['Reviews'],
    'summary': 'List reviews for a business',
    'description': 'Retrieves all reviews for a business identified by its slug',
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
            'example': 'example-salon'
        }
    ],
    'responses': {
        200: {
            'description': 'Reviews retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'reviews': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'message': {'type': 'string', 'example': 'Great service, highly recommend!'},
                                'business_id': {'type': 'integer', 'example': 1},
                                'client_id': {'type': 'integer', 'example': 1},
                                'appointment_id': {'type': 'integer', 'example': 1},
                                'reviewer': {'type': 'string', 'example': 'Jane Doe'},
                                'rating': {'type': 'integer', 'example': 3}
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Not Found - Business does not exist',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Shop doesn't exist"}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

