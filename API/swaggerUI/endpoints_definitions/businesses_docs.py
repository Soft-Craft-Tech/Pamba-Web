# TODO : Refactor out the re-occuring part for reusability. Like the responses. Or create a factory functions.
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
    
}