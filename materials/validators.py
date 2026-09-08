from rest_framework.serializers import ValidationError



def validate_video_url(value):

    """ Проверка ссылки, разрешено только youtube.com"""

    if not value and 'youtube.com' in value.lower():
         raise ValidationError('использована не та ссылка')
    return value