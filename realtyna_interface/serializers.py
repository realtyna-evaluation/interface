from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.fields import get_error_detail
from rest_framework.exceptions import ValidationError


def transform_validation_error_wrapper(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except DjangoValidationError as err:
            raise ValidationError(get_error_detail(err))

    return wrapped
