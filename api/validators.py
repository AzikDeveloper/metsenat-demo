from rest_framework.validators import ValidationError


def validate_positive(value):
    if value > 0:
        return value
    else:
        raise ValidationError('Positive integer is required')
