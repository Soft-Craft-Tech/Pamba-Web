swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"  # Swagger UI available at /docs/
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Pamba Africa API",
        "description": "API for Pamba Africa core backend",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    },
    "security": [
        {
            "ApiKeyAuth": []
        }
    ]
}