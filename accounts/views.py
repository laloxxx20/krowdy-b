from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.decorators import detail_route

from django.shortcuts import get_object_or_404

from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    EmailSerializer,
    PhoneSerializer,
    PasswordSerializer,
)
from .models import User, Email, Phone


class UserView(ModelViewSet):

    serializer_class = UserSerializer
    model = User

    def get_queryset(self):

        return self.model.objects.all()

    @detail_route(methods=['put'], serializer_class=PasswordSerializer)
    def set_password(self, request, pk=None):
        self.object = get_object_or_404(self.model, pk=pk)
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Contraseña equivocada.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(
                {'status': 'Contrasena cambiada'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailView(ModelViewSet):
    serializer_class = EmailSerializer
    model = Email

    def get_queryset(self):

        return self.model.objects.all()


class PhoneView(ModelViewSet):
    serializer_class = PhoneSerializer
    model = Phone

    def get_queryset(self):

        return self.model.objects.all()


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'first_name': user.first_name,
            'email': user.email,
            'id': user.id,
        })


obtain_auth_token = ObtainAuthToken.as_view()
