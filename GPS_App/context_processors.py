from django.conf import settings
from .models import user
from datetime import datetime


# def my_constants(request):
#     DOMAIN_NAME = settings.DOMAIN_NAME
#     DOMAIN_ICON = settings.DOMAIN_ICON
#     return {
#         'DOMAIN_NAME': DOMAIN_NAME,
#         'DOMAIN_ICON':DOMAIN_ICON
#     }

def my_constants(request):
    user_data = {}
    
    user_session = request.session.get('user')
    if user_session:
        email = user_session.get('user_email')
        if email:
            try:
                user_instance = user.objects.get(email=email)
                user_data = {
                    'id': user_instance.id,
                    'user_name': user_session.get('user_first_name'),
                    'user_email': email,
                    'first_name': user_instance.first_name,
                    'last_name': user_instance.last_name,
                    'image': user_instance.image.url if user_instance.image else None,

                }
            except user.DoesNotExist:
                user_data = {'error': 'User does not exist'}

    return {
        'user_data': user_data,
    }