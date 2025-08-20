 # Reusable response schemas
COMMON_RESPONSES = {
    400: {
        'description': 'Bad request - Invalid payload or parameters',
        'schema': {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'examples': ['Invalid payload: JSON format required', 'Invalid payload: {key} key is required']
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized - Invalid API key or credentials',
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
        'description': 'Resource not found',
        'schema': {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'Not Found'
                }
            }
        }
    },
    409: {
        'description': 'Conflict - Resource already exists',
        'schema': {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'examples': ['Email already exists', 'Phone number already exists']
                }
            }
        }
    }
}