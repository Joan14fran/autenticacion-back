from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, get_user_model


from .serializers import UserSerializer

class SignIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # Actualiza el campo last_login
                user.last_login = timezone.now()
                user.save()
                
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'mensaje': 'Inicio de sesión validado'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'El usuario no está activo'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class SignUp(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Verificar si ya existe un usuario con el mismo username o email
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            if get_user_model().objects.filter(username=username).exists() or get_user_model().objects.filter(email=email).exists():
                return Response({'error': 'El username o email ya está en uso'}, status=status.HTTP_400_BAD_REQUEST)
            # Si no hay un usuario con el mismo username o email, guardar el nuevo usuario
            serializer.save()
            return Response({'mensaje': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(ObtainAuthToken):
    def get(self, request, *args, **kwargs):
        try:
            token_key = request.GET.get('token')
            token = Token.objects.filter(key=token_key).first()
            if token:
                user = token.user
                # Eliminar todas las sesiones activas para el usuario
                all_sessions = Session.objects.filter(expire_date__gte=timezone.now(), session_key__contains=user.username)
                if all_sessions.exists():
                    for session in all_sessions:
                        session.delete()
                # Eliminar el token de autenticación
                token.delete()
                return Response({'message': 'Cierre de sesión exitoso'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No se encontró un token válido'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

