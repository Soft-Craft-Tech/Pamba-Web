from flasgger import SwaggerView
from API.lib.auth import business_login_required, business_verification_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

RECORD_INVENTORY = {
    'tags': ['Inventory'],
    'summary': 'Record a new inventory item',
    'description': 'Allows a logged-in and verified business to record a new inventory item',
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
                    'product': {'type': 'string', 'description': 'Name of the inventory item', 'example': 'Shampoo'}
                },
                'required': ['product']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Inventory item recorded successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Inventory created'},
                    'inventory': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'product': {'type': 'string', 'example': 'Shampoo'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'string', 'example': None},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'updated_at': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

DELETE_INVENTORY = {
    'tags': ['Inventory'],
    'summary': 'Delete an inventory item',
    'description': 'Allows a logged-in and verified business to delete an inventory item by ID',
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
            'name': 'inventory_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the inventory item to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Inventory item deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Deleted'},
                    'inventory': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'product': {'type': 'string', 'example': 'Shampoo'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'string', 'example': None},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'updated_at': {'type': 'string', 'example': None}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this inventory item',
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

UPDATE_INVENTORY_STATUS = {
    'tags': ['Inventory'],
    'summary': 'Update inventory item status',
    'description': 'Allows a logged-in and verified business to update the status of an inventory item (Critical, Low, Normal)',
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
            'name': 'inventory_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the inventory item to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'description': 'Status of the inventory item', 'example': 'Low', 'enum': ['Critical', 'Low', 'Normal']}
                },
                'required': ['status']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Inventory status updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Updated'},
                    'inventory': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'product': {'type': 'string', 'example': 'Shampoo'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'string', 'example': 'Low'},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                            'updated_at': {'type': 'string', 'example': '2025-08-13T12:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request - Status not recognized',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Status not recognized'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to update this inventory item',
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

FETCH_ALL_RECORDS = {
    'tags': ['Inventory'],
    'summary': 'Fetch all inventory records for a business',
    'description': 'Retrieves all inventory records associated with the logged-in business',
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
            'description': 'Inventory records retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'inventory': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'product': {'type': 'string', 'example': 'Shampoo'},
                                'business_id': {'type': 'integer', 'example': 1},
                                'status': {'type': 'string', 'example': 'Normal'},
                                'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'},
                                'updated_at': {'type': 'string', 'example': None}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

