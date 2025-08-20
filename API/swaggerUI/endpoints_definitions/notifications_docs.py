from flasgger import SwaggerView
from API.lib.auth import client_login_required, business_login_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

ADD_CLIENT_NOTIFICATION = {
    'tags': ['Notifications'],
    'summary': 'Create a notification for a client',
    'description': 'Creates a new notification for a specified client',
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
                    'title': {'type': 'string', 'description': 'Title of the notification', 'example': 'Appointment Reminder'},
                    'message': {'type': 'string', 'description': 'Message content of the notification', 'example': 'Your appointment is scheduled for tomorrow at 10 AM'},
                    'clientID': {'type': 'integer', 'description': 'ID of the client receiving the notification', 'example': 1}
                },
                'required': ['title', 'message', 'clientID']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Notification created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification sent'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

READ_CLIENT_NOTIFICATION = {
    'tags': ['Notifications'],
    'summary': 'Mark a client notification as read',
    'description': 'Allows a logged-in client to mark a specific notification as read',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated client'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the notification to mark as read'
        }
    ],
    'responses': {
        200: {
            'description': 'Notification marked as read successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification Read'},
                    'notification': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'title': {'type': 'string', 'example': 'Appointment Reminder'},
                            'message': {'type': 'string', 'example': 'Your appointment is scheduled for tomorrow at 10 AM'},
                            'client_id': {'type': 'integer', 'example': 1},
                            'read': {'type': 'boolean', 'example': True},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request - Notification is already read',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification is already Read'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to access this notification',
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

DELETE_CLIENT_NOTIFICATION = {
    'tags': ['Notifications'],
    'summary': 'Delete a client notification',
    'description': 'Allows a logged-in client to delete a specific notification',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated client'
        },
        {
            'name': 'X-API-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API Key for authentication'
        },
        {
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the notification to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Notification deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification deleted'},
                    'notification': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'title': {'type': 'string', 'example': 'Appointment Reminder'},
                            'message': {'type': 'string', 'example': 'Your appointment is scheduled for tomorrow at 10 AM'},
                            'client_id': {'type': 'integer', 'example': 1},
                            'read': {'type': 'boolean', 'example': False},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this notification',
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

FETCH_ALL_CLIENT_NOTIFICATIONS = {
    'tags': ['Notifications'],
    'summary': 'Fetch all client notifications',
    'description': 'Retrieves all notifications for the logged-in client',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token for authenticated client'
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
            'description': 'Notifications retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'notifications': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'title': {'type': 'string', 'example': 'Appointment Reminder'},
                                'message': {'type': 'string', 'example': 'Your appointment is scheduled for tomorrow at 10 AM'},
                                'client_id': {'type': 'integer', 'example': 1},
                                'read': {'type': 'boolean', 'example': False},
                                'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

ADD_BUSINESS_NOTIFICATION = {
    'tags': ['Notifications'],
    'summary': 'Create a notification for a business',
    'description': 'Creates a new notification for a specified business',
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
                    'title': {'type': 'string', 'description': 'Title of the notification', 'example': 'New Booking'},
                    'message': {'type': 'string', 'description': 'Message content of the notification', 'example': 'A new booking has been made for your salon'},
                    'businessID': {'type': 'integer', 'description': 'ID of the business receiving the notification', 'example': 1}
                },
                'required': ['title', 'message', 'businessID']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Notification created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification sent'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

READ_BUSINESS_NOTIFICATION = {
    'tags': ['Notifications'],
    'summary': 'Mark a business notification as read',
    'description': 'Allows a logged-in business to mark a specific notification as read',
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
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the notification to mark as read'
        }
    ],
    'responses': {
        200: {
            'description': 'Notification marked as read successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification Read'},
                    'notification': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'title': {'type': 'string', 'example': 'New Booking'},
                            'message': {'type': 'string', 'example': 'A new booking has been made for your salon'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'read': {'type': 'boolean', 'example': True},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request - Notification is already read',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Notification is already Read'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to access this notification',
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

DELETE_BUSINESS_NOTIFICATION = {
    'tags': ['Notifications'],
    'summary': 'Delete a business notification',
    'description': 'Allows a logged-in business to delete a specific notification',
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
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the notification to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Notification deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Deleted'},
                    'notification': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'title': {'type': 'string', 'example': 'New Booking'},
                            'message': {'type': 'string', 'example': 'A new booking has been made for your salon'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'read': {'type': 'boolean', 'example': False},
                            'created_at': {'type': 'string', 'example': '2025-08-13T00:00:00'}
                        }
                    }
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this notification',
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

