from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if not username or not email or not password or not first_name or not last_name:
            return Response(
                {"error": "Todos os campos são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email já está em uso."}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User(
            username=username,
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
        )
        user.save()

        return Response(
            {"success": "Conta criada com sucesso."}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"success": "Login realizado com sucesso."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logout realizado com sucesso."}, status=status.HTTP_200_OK
        )
