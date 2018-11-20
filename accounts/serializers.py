from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from accounts.models import User, Email, Phone


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ('id', 'email', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', None)
        if context:
            request = context.get('request', None)
            self.main_email = bool(request.GET.get('main_email', False))

    def update(self, instance, validated_data):
        if self.main_email:
            instance.user.email = validated_data.get('email', instance.email)
            instance.user.main_id_email = validated_data.get(
                'id', instance.id)
            instance.user.save()

        return instance


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = ('id', 'phone', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', None)
        if context:
            request = context.get('request', None)
            self.main_phone = bool(request.GET.get('main_phone', False))

    def update(self, instance, validated_data):
        if self.main_phone:
            instance.user.phone = validated_data.get('phone', instance.phone)
            instance.user.main_id_phone = validated_data.get(
                'id', instance.id)
            instance.user.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    emails = EmailSerializer(many=True, required=False)
    phones = PhoneSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'main_id_email',
            'phone',
            'main_id_phone',
            'password',
            'first_name',
            'emails',
            'phones',
        )

    def create(self, validated_data):
        emails_data = []
        if 'emails' in validated_data:
            emails_data = validated_data.pop('emails')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        email_obj = Email.objects.create(user=user, email=user.email)
        user.main_id_email = email_obj.id
        user.save()
        for email in emails_data:
            Email.objects.create(user=user, **email)
        return user


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
