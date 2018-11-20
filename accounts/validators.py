from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class PhoneValidator(RegexValidator):
    """
    Helper class to validate if an input is a valid phone number.
    Regex explanation:
        - Value may start with `+51` followed by either an `8` or `9`
          and 8 extra digits after that.
    """
    regex = r'^((\+51)|(\+59))?[89]\d{8}$'
    message = _('Ingresa un número de celular válido')
