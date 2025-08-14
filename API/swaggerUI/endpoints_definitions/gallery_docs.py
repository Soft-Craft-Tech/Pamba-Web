
from flasgger import SwaggerView
from API.lib.auth import verify_api_key, business_login_required, business_verification_required
from API.swaggerUI.common_responses import COMMON_RESPONSES

FETCH_BUSINESS_GALLERY = {
    'tags': ['Gallery'],
    'summary': 'Fetch business gallery images',
    'description': 'Retrieves all gallery images for a business identified by its slug',
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
            'example': 'example-business'
        }
    ],
    'responses': {
        200: {
            'description': 'Gallery images retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'gallery': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'image_url': {'type': 'string', 'example': 'https://example.com/images/gallery1.jpg'},
                                'business_id': {'type': 'integer', 'example': 1},
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

ADD_GALLERY_IMAGE = {
    'tags': ['Gallery'],
    'summary': 'Add an image to business gallery',
    'description': 'Allows a logged-in and verified business to add an image to its gallery',
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
                    'imgURL': {'type': 'string', 'description': 'URL of the image to add', 'example': 'https://example.com/images/gallery2.jpg'}
                },
                'required': ['imgURL']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Image added successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Image Added'}
                }
            }
        },
        **COMMON_RESPONSES
    }
}

DELETE_GALLERY_IMAGE = {
    'tags': ['Gallery'],
    'summary': 'Delete an image from business gallery',
    'description': 'Allows a logged-in business to delete an image from its gallery by ID',
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
            'name': 'image_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the image to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Image deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Image deleted'}
                }
            }
        },
        403: {
            'description': 'Forbidden - Not allowed to delete this image',
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

# Apply Swagger documentation to endpoints
class FetchBusinessGalleryView(SwaggerView):
    decorators = [verify_api_key]
    definitions = FETCH_BUSINESS_GALLERY

class AddGalleryImageView(SwaggerView):
    decorators = [business_login_required, business_verification_required]
    definitions = ADD_GALLERY_IMAGE

class DeleteGalleryImageView(SwaggerView):
    decorators = [business_login_required]
    definitions = DELETE_GALLERY_IMAGE
