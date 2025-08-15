"""
OAuth2 Provider Settings
"""

# OAuth2 Provider Configuration
OAUTH2_PROVIDER = {
    # OAuth2 scopes
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
    },
    # Token settings
    "ACCESS_TOKEN_EXPIRE_SECONDS": 36_000,  # 10 hours
    "REFRESH_TOKEN_EXPIRE_SECONDS": 1_209_600,  # 14 days
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 600,  # 10 minutes
    # Application settings
    "CLIENT_ID_GENERATOR_CLASS": "oauth2_provider.generators.ClientIdGenerator",
    "CLIENT_SECRET_GENERATOR_CLASS": "oauth2_provider.generators.ClientSecretGenerator",
    "CLIENT_SECRET_GENERATOR_LENGTH": 128,
    # Security settings
    "ALLOWED_REDIRECT_URI_SCHEMES": ["http", "https"],
    "ALLOWED_SCHEMES": ["https"],
    "ALLOW_URI_WILDCARDS": False,
    # Server settings
    "OAUTH2_SERVER_CLASS": "oauthlib.oauth2.Server",
    "OAUTH2_VALIDATOR_CLASS": "oauth2_provider.oauth2_validators.OAuth2Validator",
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.OAuthLibCore",
    # Extra settings
    "EXTRA_SERVER_KWARGS": {},
}

# Login URL for OAuth2
LOGIN_URL = "/admin/login/"
