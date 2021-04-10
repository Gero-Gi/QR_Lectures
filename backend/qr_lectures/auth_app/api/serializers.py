from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import LazyObject
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.exceptions import NotFound

from auth_app.models import UserDevice



class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    udi = serializers.CharField(
        label=_("UDI"),
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        udi = attrs.get('udi')

        if not udi:
            msg = _('Must include "UDI".')
            raise serializers.ValidationError(msg, code='authorization')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            user_device = None
            try:
                user_device = UserDevice.objects.get(user=user)
            except ObjectDoesNotExist:
                user_device = UserDevice.objects.create(
                    user=user,
                    udi=udi
                )

                
            if not user_device.check_udi(udi):
                msg = _('UDI does not match')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
