import re

from rest_framework_simplejwt import serializers

from api.utils import ME, PATTERN


class ValidateUsername:

    def validate_username(self, value):
        if value == ME or not re.match(PATTERN, value):
            raise serializers.ValidationError(
                ['Недопустимый username']
            )
        return value
