from rest_framework.serializers import ValidationError


# def validate_link(data):
#     link = data.get('link')
#     print(link)
#     if not link.startswith('https://www.youtube.com/'):
#         raise ValidationError('Ссылка не может быть добавлена')

class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if 'youtube' not in tmp_val:
            raise ValidationError('Ссылка не может быть добавлена')
