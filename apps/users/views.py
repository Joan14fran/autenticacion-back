from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

from .serializers import UserSerializer

class SignIn(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
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

class SignUp(APIView):
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
