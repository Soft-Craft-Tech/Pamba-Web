from flasgger import SwaggerView
from API.lib.auth import verify_api_key

# Import common responses from existing file
from API.swaggerUI.common_responses import COMMON_RESPONSES

ADD_RATING = {
    'tags': ['Ratings'],
    'summary': 'Add a rating to a business',
    'description': 'Allows a client to post a rating for a business identified by its ID',
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
                    'rating': {'type': 'integer', 'description': 'Rating value (e.g., 1 to 5)', 'example': 5},
                    'businessID': {'type': 'integer', 'description': 'ID of the business being rated', 'example': 1}
                },
                'required': ['rating', 'businessID']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Rating posted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Rating has been posted'}
                }
            }
        },
        400: {
            'description': 'Bad Request - Invalid payload or rating value',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Invalid payload: 'rating' key is required"}
                }
            }
        },
        404: {
            'description': 'Not Found - Business does not exist',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Business doesn't exist"}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

