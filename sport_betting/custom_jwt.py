from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'username': user.phone,
        'is_admin': user.is_staff,
        'user': {
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'phone': user.phone,
            'profile_image': str(user.profile_image),
            'calling_code': user.calling_code,
            'is_admin': user.is_staff,
        },
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    return {
        'token': token,
        'user': {
            'email': user.email,
            'user_id': user.pk,
            'username': user.username,
            'phone': user.phone,
            'profile_image': str(user.profile_image),
            'calling_code': user.calling_code,
            'is_admin': user.is_staff,
        }
    }
