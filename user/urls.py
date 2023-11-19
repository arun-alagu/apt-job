from django.urls import path

from user import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

app_name = "user"

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('register/employer/', views.CreateEmployerView.as_view(),
         name='employer-register'),
    path('account/', views.ManageUserView.as_view(), name='users-account'),
    # path("create/", views.CreateUserView.as_view(), name="create"),
    # path("token/", views.CreateTokenView.as_view(), name="token"),
    # path("me/", views.ManageUserView.as_view(), name="users-profile")
]
