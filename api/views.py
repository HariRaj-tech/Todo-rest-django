# api/views.py
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from todo.models import Todo
from .serializers import TodoSerializer, TodoToggleCompleteSerializer


class TodoListCreate(generics.ListCreateAPIView):
    # Permissions
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user
        print("GETTED")
        return Todo.objects.filter(user=user).order_by("-created")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class TodoRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-created")


class TodoToggleComplete(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoToggleCompleteSerializer

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not (serializer.instance.completed)
        serializer.save()
        return super().perform_update(serializer)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            print(data)
            user = get_user_model().objects.create_user(
                username=data["username"], password=data["password"]
            )
            user.save()

            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)

        except IntegrityError:
            return JsonResponse(
                {"error": "Username already taken, choose another username"}, status=400
            )


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = authenticate(
            request,
            username=data["username"],
            password=data["password"],
        )
        if user is None:
            return JsonResponse(
                {"error": "unable to login, check username and password"}
            )
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            finally:
                return JsonResponse({"token": str(token)}, status=201)
    else:
        print("Called using ", request.method)
        return JsonResponse({"error": f"Method {request.method} not allowed, only POST"}, status=401)
