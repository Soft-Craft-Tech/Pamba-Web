from flasgger import SwaggerView
from API.lib.auth import business_login_required, business_verification_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

RECORD_SALE = {
    'tags': ['Sales'],
    'summary': 'Record a new sale',
    'description': 'Allows a logged-in and verified business to record a new sale for a service',
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
                    'paymentMethod': {'type': 'string', 'description': 'Payment method for the sale', 'example': 'Cash'},
                    'description': {'type': 'string', 'description': 'Description of the sale', 'example': 'Haircut service payment'},
                    'serviceId': {'type': 'integer', 'description': 'ID of the service', 'example': 1}
                },
                'required': ['paymentMethod', 'description', 'serviceId']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Sale recorded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Sale Added'},
                    'newSale': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'payment_method': {'type': 'string', 'example': 'Cash'},
                            'description': {'type': 'string', 'example': 'Haircut service payment'},
                            'service_id': {'type': 'integer', 'example': 1},
                            'business_id': {'type': 'integer', 'example': 1},
                            'date_created': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request - Service not offered by the business',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'We are not offering this service at the moment'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_ALL_BUSINESS_SALES = {
    'tags': ['Sales'],
    'summary': 'Fetch all sales for a business',
    'description': 'Retrieves all sales associated with the logged-in and verified business, including service details',
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
            'description': 'Sales retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Sales'},
                    'sales': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'payment_method': {'type': 'string', 'example': 'Cash'},
                                'description': {'type': 'string', 'example': 'Haircut service payment'},
                                'service_id': {'type': 'integer', 'example': 1},
                                'business_id': {'type': 'integer', 'example': 1},
                                'date_created': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                                'service': {'type': 'string', 'example': 'Haircut'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

DELETE_SALE = {
    'tags': ['Sales'],
    'summary': 'Delete a sale',
    'description': 'Allows a logged-in and verified business to delete a sale by ID',
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
            'name': 'sale_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the sale to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Sale deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Sale deleted'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this sale',
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

REVENUE_ANALYTICS = {
    'tags': ['Sales'],
    'summary': 'Business revenue analysis',
    'description': 'Provides revenue analytics for the logged-in and verified business, including lifetime sales, total sales, current month revenue, and last 7 days sales',
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
            'description': 'Revenue analytics retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'lifetime_sales': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'payment_method': {'type': 'string', 'example': 'Cash'},
                                'description': {'type': 'string', 'example': 'Haircut service payment'},
                                'service_id': {'type': 'integer', 'example': 1},
                                'business_id': {'type': 'integer', 'example': 1},
                                'date_created': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                                'price': {'type': 'number', 'example': 20.0}
                            }
                        }
                    },
                    'total_sales': {'type': 'number', 'example': 1000.0},
                    'current_month_revenue': {'type': 'number', 'example': 500.0},
                    'last_seven_days': {'type': 'number', 'example': 200.0}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

EDIT_SALE = {
    'tags': ['Sales'],
    'summary': 'Edit a sale',
    'description': 'Allows a logged-in and verified business to update a sale’s payment method, description, or service ID',
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
            'name': 'sale_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the sale to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': {
                'type': 'object',
                'properties': {
                    'paymentmethod': {'type': 'string', 'description': 'Updated payment method for the sale', 'example': 'Card'},
                    'description': {'type': 'string', 'description': 'Updated description of the sale', 'example': 'Updated haircut service payment'},
                    'service_id': {'type': 'integer', 'description': 'Updated ID of the service', 'example': 2}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Sale updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Sale updated'},
                    'updatedSale': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'payment_method': {'type': 'string', 'example': 'Card'},
                            'description': {'type': 'string', 'example': 'Updated haircut service payment'},
                            'service_id': {'type': 'integer', 'example': 2},
                            'business_id': {'type': 'integer', 'example': 1},
                            'date_created': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request - Service does not exist or not allowed',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Service does not exist!'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to update this sale',
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

