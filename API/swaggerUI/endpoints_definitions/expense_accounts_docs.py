from flasgger import SwaggerView
from API.lib.auth import business_login_required, business_verification_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

CREATE_EXPENSE_ACCOUNT = {
    'tags': ['Accounts'],
    'summary': 'Create expense accounts for a business',
    'description': 'Allows a logged-in and verified business to create one or more expense accounts',
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
                    'accounts': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'accountName': {'type': 'string', 'description': 'Name of the expense account', 'example': 'Utilities'},
                                'description': {'type': 'string', 'description': 'Description of the expense account', 'example': 'Monthly utility expenses'}
                            },
                            'required': ['accountName', 'description']
                        }
                    }
                },
                'required': ['accounts']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Accounts created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Accounts have been created'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

DELETE_ACCOUNT = {
    'tags': ['Accounts'],
    'summary': 'Delete a business expense account',
    'description': 'Allows a logged-in and verified business to delete an expense account by ID, after password verification',
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
            'name': 'account_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the expense account to delete'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'password': {'type': 'string', 'description': 'Business password for verification', 'example': 'securepassword123'}
                },
                'required': ['password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Account deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Account Deleted'}
                }
            }
        },
        401: {
            'description': 'Unauthorized - Incorrect password',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Incorrect password'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this account',
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

UPDATE_ACCOUNT = {
    'tags': ['Accounts'],
    'summary': 'Update an expense account',
    'description': 'Allows a logged-in and verified business to update an expense account’s name and description, after password verification',
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
            'name': 'account_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the expense account to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'accountName': {'type': 'string', 'description': 'New name of the expense account', 'example': 'Utilities Updated'},
                    'description': {'type': 'string', 'description': 'New description of the expense account', 'example': 'Updated monthly utility expenses'},
                    'password': {'type': 'string', 'description': 'Business password for verification', 'example': 'securepassword123'}
                },
                'required': ['accountName', 'description', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Account updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Account Updated'}
                }
            }
        },
        401: {
            'description': 'Unauthorized - Incorrect password',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Incorrect password'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to update this account',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Not allowed'}
                }
            }
        },
        409: {
            'description': 'Conflict - Account name already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'This account name already exists'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_ALL_BUSINESS_ACCOUNTS = {
    'tags': ['Accounts'],
    'summary': 'Fetch all expense accounts for a business',
    'description': 'Retrieves all expense accounts associated with the logged-in and verified business',
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
            'description': 'Accounts retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'account': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'account_name': {'type': 'string', 'example': 'Utilities'},
                                'description': {'type': 'string', 'example': 'Monthly utility expenses'},
                                'business_id': {'type': 'integer', 'example': 1}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

