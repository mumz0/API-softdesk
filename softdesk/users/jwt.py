from rest_framework_simplejwt.authentication import JWTAuthentication

def custom_authentication_rule(user):
    return user.is_active and user.email_verified

JWT_AUTHENTICATION_RULE = custom_authentication_rule
