"""
Serializers para registro, login y datos de usuario.
Se personaliza el token JWT para incluir el claim 'rol'.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'rut']
        read_only_fields = ['id']


class RegistroSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevos usuarios desde la API."""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'rol', 'rut']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer JWT personalizado: agrega el rol y el username
    como claims dentro del token de acceso.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims personalizados
        token['rol'] = user.rol
        token['username'] = user.username
        token['email'] = user.email or ''
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Además del token, enviamos datos del usuario
        data['usuario'] = {
            'id': self.user.id,
            'username': self.user.username,
            'rol': self.user.rol,
        }
        return data