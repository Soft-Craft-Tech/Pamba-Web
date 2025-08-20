from flasgger import SwaggerView
from API.lib.auth import business_login_required, business_verification_required

# Import common responses from existing file
from API.swaggerUI.common_responses import COMMON_RESPONSES

RECORD_EXPENSE = {
    'tags': ['Expenses'],
    'summary': 'Record a new expense',
    'description': 'Allows a logged-in and verified business to record a new expense associated with an expense account',
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
                    'expenseTitle': {'type': 'string', 'description': 'Title of the expense', 'example': 'Electricity Bill'},
                    'expenseAmount': {'type': 'number', 'description': 'Amount of the expense', 'example': 150.50},
                    'description': {'type': 'string', 'description': 'Description of the expense', 'example': 'Monthly electricity bill for the shop'},
                    'accountID': {'type': 'integer', 'description': 'ID of the expense account', 'example': 1}
                },
                'required': ['expenseTitle', 'expenseAmount', 'description', 'accountID']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Expense recorded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Expense Recorded'},
                    'expense': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'expense': {'type': 'string', 'example': 'Electricity Bill'},
                            'amount': {'type': 'number', 'example': 150.50},
                            'description': {'type': 'string', 'example': 'Monthly electricity bill for the shop'},
                            'expense_account': {'type': 'integer', 'example': 1},
                            'business_id': {'type': 'integer', 'example': 1},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'modified_at': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to access this expense account',
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

DELETE_EXPENSE = {
    'tags': ['Expenses'],
    'summary': 'Delete an expense',
    'description': 'Allows a logged-in and verified business to delete an expense by ID',
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
            'name': 'expense_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the expense to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Expense deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Expense deleted'},
                    'deleted': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'expense': {'type': 'string', 'example': 'Electricity Bill'},
                            'amount': {'type': 'number', 'example': 150.50},
                            'description': {'type': 'string', 'example': 'Monthly electricity bill for the shop'},
                            'expense_account': {'type': 'integer', 'example': 1},
                            'business_id': {'type': 'integer', 'example': 1},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'modified_at': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

UPDATE_EXPENSE = {
    'tags': ['Expenses'],
    'summary': 'Update an expense',
    'description': 'Allows a logged-in and verified business to update an expense’s details',
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
            'name': 'expense_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the expense to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'expenseTitle': {'type': 'string', 'description': 'Updated title of the expense', 'example': 'Electricity Bill Updated'},
                    'expenseAmount': {'type': 'number', 'description': 'Updated amount of the expense', 'example': 175.75},
                    'description': {'type': 'string', 'description': 'Updated description of the expense', 'example': 'Updated monthly electricity bill'},
                    'accountID': {'type': 'integer', 'description': 'Updated ID of the expense account', 'example': 1}
                },
                'required': ['expenseTitle', 'expenseAmount', 'description', 'accountID']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Expense updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Update Successful'},
                    'updated': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'expense': {'type': 'string', 'example': 'Electricity Bill Updated'},
                            'amount': {'type': 'number', 'example': 175.75},
                            'description': {'type': 'string', 'example': 'Updated monthly electricity bill'},
                            'expense_account': {'type': 'integer', 'example': 1},
                            'business_id': {'type': 'integer', 'example': 1},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'modified_at': {'type': 'string', 'example': '2025-08-13T12:00:00'}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_BUSINESS_EXPENSES = {
    'tags': ['Expenses'],
    'summary': 'Fetch all expenses for a business',
    'description': 'Retrieves all expenses associated with the logged-in and verified business, including the account category',
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
            'description': 'Expenses retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'expenses': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'expense': {'type': 'string', 'example': 'Electricity Bill'},
                                'amount': {'type': 'number', 'example': 150.50},
                                'description': {'type': 'string', 'example': 'Monthly electricity bill for the shop'},
                                'expense_account': {'type': 'integer', 'example': 1},
                                'business_id': {'type': 'integer', 'example': 1},
                                'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                                'modified_at': {'type': 'string', 'example': None},
                                'category': {'type': 'string', 'example': 'Utilities'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_SINGLE_EXPENSE = {
    'tags': ['Expenses'],
    'summary': 'Fetch a single expense',
    'description': 'Retrieves details of a specific expense by ID for a logged-in and verified business',
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
            'name': 'expense_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the expense to fetch'
        }
    ],
    'responses': {
        200: {
            'description': 'Expense retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'expense': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'expense': {'type': 'string', 'example': 'Electricity Bill'},
                            'amount': {'type': 'number', 'example': 150.50},
                            'description': {'type': 'string', 'example': 'Monthly electricity bill for the shop'},
                            'expense_account': {'type': 'integer', 'example': 1},
                            'business_id': {'type': 'integer', 'example': 1},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'modified_at': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to access this expense',
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

