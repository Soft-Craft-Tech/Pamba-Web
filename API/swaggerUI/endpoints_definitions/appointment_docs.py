from flasgger import SwaggerView
from API.swaggerUI.common_responses import COMMON_RESPONSES

from API.lib.auth import verify_api_key, client_login_required, business_login_required, business_verification_required


BOOK_APPOINTMENT = {
    'tags': ['Appointments'],
    'summary': 'Book an appointment from the mobile application',
    'description': 'Allows a logged-in client to book an appointment with a business, optionally specifying a staff member',
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
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'date': {'type': 'string', 'description': 'Appointment date (DD-MM-YYYY)', 'example': '25-12-2025'},
                    'time': {'type': 'string', 'description': 'Appointment time (HH:MM)', 'example': '14:30'},
                    'comment': {'type': 'string', 'description': 'Optional comment for the appointment', 'example': 'Prefer quick service'},
                    'service': {'type': 'integer', 'description': 'Service ID', 'example': 1},
                    'staff': {'type': 'integer', 'description': 'Optional staff ID', 'example': 2}
                },
                'required': ['date', 'time', 'service']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment booked successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Booking Successful. Check your email for confirmation details'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

BOOK_APPOINTMENT_ON_WEB = {
    'tags': ['Appointments'],
    'summary': 'Book an appointment from the web without authentication',
    'description': 'Allows unauthenticated users to book an appointment by providing client details',
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
                    'date': {'type': 'string', 'description': 'Appointment date (DD-MM-YYYY)', 'example': '25-12-2025'},
                    'time': {'type': 'string', 'description': 'Appointment time (HH:MM)', 'example': '14:30'},
                    'comment': {'type': 'string', 'description': 'Optional comment for the appointment', 'example': 'Prefer quick service'},
                    'business': {'type': 'integer', 'description': 'Business ID', 'example': 1},
                    'service': {'type': 'integer', 'description': 'Service ID', 'example': 1},
                    'staff': {'type': 'integer', 'description': 'Optional staff ID', 'example': 2},
                    'email': {'type': 'string', 'description': 'Client email', 'example': 'client@example.com'},
                    'phone': {'type': 'string', 'description': 'Client phone number', 'example': '+254123456789'},
                    'name': {'type': 'string', 'description': 'Client name', 'example': 'John Doe'},
                    'notification': {'type': 'string', 'description': 'Notification mode (e.g., sms, whatsapp)', 'example': 'sms'}
                },
                'required': ['date', 'time', 'business', 'service', 'email', 'phone', 'name', 'notification']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment booked successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Booking Successful. Check your email for confirmation details'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

RESCHEDULE_APPOINTMENT = {
    'tags': ['Appointments'],
    'summary': 'Reschedule an existing appointment',
    'description': 'Allows a logged-in client to reschedule an appointment, updating date, time, staff, or comment',
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
            'name': 'appointment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the appointment to reschedule'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'date': {'type': 'string', 'description': 'New appointment date (DD-MM-YYYY)', 'example': '25-12-2025'},
                    'time': {'type': 'string', 'description': 'New appointment time (HH:MM)', 'example': '14:30'},
                    'notification': {'type': 'string', 'description': 'Optional notification mode', 'example': 'sms'},
                    'comment': {'type': 'string', 'description': 'Optional comment for the appointment', 'example': 'Updated request'},
                    'staff_id': {'type': 'integer', 'description': 'Optional new staff ID', 'example': 2}
                },
                'required': ['date', 'time']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment rescheduled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Appointment has been rescheduled'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

CANCEL_APPOINTMENT = {
    'tags': ['Appointments'],
    'summary': 'Cancel an appointment',
    'description': 'Allows a logged-in client to cancel an existing appointment',
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
            'name': 'appointment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the appointment to cancel'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'comment': {'type': 'string', 'description': 'Optional comment for cancellation', 'example': 'No longer needed'}
                },
                'required': ['comment']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment cancelled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Cancellation Successful'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

MY_APPOINTMENTS = {
    'tags': ['Appointments'],
    'summary': 'Fetch client’s appointments',
    'description': 'Retrieve all appointments for a logged-in client, categorized as cancelled, upcoming, and previous',
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
            'description': 'Appointments retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Success'},
                    'cancelled': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'date': {'type': 'string', 'example': '2025-08-12'},
                                'time': {'type': 'string', 'example': '14:30:00'},
                                'comment': {'type': 'string', 'example': 'No longer needed'},
                                'business_id': {'type': 'integer', 'example': 1},
                                'client_id': {'type': 'integer', 'example': 1},
                                'staff_id': {'type': 'integer', 'example': 2},
                                'service_id': {'type': 'integer', 'example': 1},
                                'cancelled': {'type': 'boolean', 'example': True},
                                'completed': {'type': 'boolean', 'example': False},
                                'imgUrl': {'type': 'string', 'example': 'https://example.com/image.jpg'},
                                'phone': {'type': 'string', 'example': '+254123456789'},
                                'name': {'type': 'string', 'example': 'Pamba Salon'},
                                'description': {'type': 'string', 'example': '123 Main St, Nairobi'},
                                'placeId': {'type': 'string', 'example': 'ChIJ...'},
                                'directions': {'type': 'string', 'example': 'https://www.google.com/maps/dir/?api=1&destination=-1.292066,36.821946'}
                            }
                        }
                    },
                    'upcoming': {'type': 'array', 'items': {'$ref': '#/definitions/Appointment'}},
                    'previous': {'type': 'array', 'items': {'$ref': '#/definitions/Appointment'}}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

ASSIGN_APPOINTMENT = {
    'tags': ['Appointments'],
    'summary': 'Assign an appointment to a staff member',
    'description': 'Allows a logged-in and verified business to assign an appointment to a staff member',
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
            'name': 'appointment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the appointment to assign'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'staffID': {'type': 'integer', 'description': 'ID of the staff member to assign', 'example': 2},
                    'password': {'type': 'string', 'description': 'Business password for verification', 'example': 'securepassword123'}
                },
                'required': ['staffID', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment assigned successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Successful'},
                    'appointment': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'date': {'type': 'string', 'example': '2025-08-12'},
                            'time': {'type': 'string', 'example': '14:30:00'},
                            'comment': {'type': 'string', 'example': 'Prefer quick service'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'client_id': {'type': 'integer', 'example': 1},
                            'staff_id': {'type': 'integer', 'example': 2},
                            'service_id': {'type': 'integer', 'example': 1},
                            'cancelled': {'type': 'boolean', 'example': False},
                            'completed': {'type': 'boolean', 'example': False}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_BUSINESS_APPOINTMENTS = {
    'tags': ['Appointments'],
    'summary': 'Fetch all appointments for a business',
    'description': 'Retrieve all non-cancelled appointments for a logged-in and verified business',
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
            'description': 'Appointments retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'appointments': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'date': {'type': 'string', 'example': '2025-08-12'},
                                'time': {'type': 'string', 'example': '14:30:00'},
                                'comment': {'type': 'string', 'example': 'Prefer quick service'},
                                'business_id': {'type': 'integer', 'example': 1},
                                'client_id': {'type': 'integer', 'example': 1},
                                'staff_id': {'type': 'integer', 'example': 2},
                                'service_id': {'type': 'integer', 'example': 1},
                                'cancelled': {'type': 'boolean', 'example': False},
                                'completed': {'type': 'boolean', 'example': False},
                                'start': {'type': 'string', 'example': '2025-08-12 14:30'},
                                'end': {'type': 'string', 'example': '2025-08-12 15:00'},
                                'people': {'type': 'array', 'items': {'type': 'string', 'example': 'John Doe'}},
                                'title': {'type': 'string', 'example': 'Haircut by Jane'},
                                'calendarId': {'type': 'string', 'example': 'upcoming'}
                            }
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

END_APPOINTMENT = {
    'tags': ['Appointments'],
    'summary': 'End an appointment',
    'description': 'Allows a logged-in and verified business to mark an appointment as completed and trigger a review request',
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
            'name': 'appointment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the appointment to end'
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment ended successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Appointment ended. Review request email sent to the client.'},
                    'appointment': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'date': {'type': 'string', 'example': '2025-08-12'},
                            'time': {'type': 'string', 'example': '14:30:00'},
                            'comment': {'type': 'string', 'example': 'Prefer quick service'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'client_id': {'type': 'integer', 'example': 1},
                            'staff_id': {'type': 'integer', 'example': 2},
                            'service_id': {'type': 'integer', 'example': 1},
                            'cancelled': {'type': 'boolean', 'example': False},
                            'completed': {'type': 'boolean', 'example': True}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

FETCH_SINGLE_APPOINTMENT = {
    'tags': ['Appointments'],
    'summary': 'Fetch a single appointment',
    'description': 'Retrieve details of a specific appointment by its ID',
    'parameters': [
        {
            'name': 'appointment_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the appointment'
        }
    ],
    'responses': {
        200: {
            'description': 'Appointment retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'appointment': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'date': {'type': 'string', 'example': '2025-08-12'},
                            'time': {'type': 'string', 'example': '14:30:00'},
                            'comment': {'type': 'string', 'example': 'Prefer quick service'},
                            'business_id': {'type': 'integer', 'example': 1},
                            'client_id': {'type': 'integer', 'example': 1},
                            'staff_id': {'type': 'integer', 'example': 2},
                            'service_id': {'type': 'integer', 'example': 1},
                            'cancelled': {'type': 'boolean', 'example': False},
                            'completed': {'type': 'boolean', 'example': False}
                        }
                    }
                }
            }
        },
        **COMMON_RESPONSES
    }
}

SEND_APPOINTMENT_REMINDER = {
    'tags': ['Appointments'],
    'summary': 'Send reminders for upcoming appointments',
    'description': 'Sends SMS or WhatsApp reminders for appointments scheduled for today',
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
            'description': 'Reminders sent successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Sent successfully'},
                    'unsuccessful': {'type': 'integer', 'example': 0}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

