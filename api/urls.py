from django.urls import path

from .views import (
    TodoListCreate,
    TodoRetrieveUpdateDestory,
    TodoToggleComplete,
    signup,
    login,
)

urlpatterns = [
    path("", TodoListCreate.as_view(), name="list-view"),
    path("<int:pk>", TodoRetrieveUpdateDestory.as_view(), name="list"),
    path("<int:pk>/complete", TodoToggleComplete.as_view(), name="list"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
]
