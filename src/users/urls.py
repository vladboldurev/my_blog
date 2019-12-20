from django.urls import path
from .views import (
        RegisterUserView, ChangeUserInfoView, UserProfile,
        RegisterDoneView, RegisterActivateView, DeleteUserView
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/done', RegisterDoneView.as_view(), name='register_done'),
    path('<int:pk>/profile', UserProfile.as_view(), name='profile'),
    path('<int:pk>/change_user_info', ChangeUserInfoView.as_view(), name='change_user_info'),
    path('register/activate/<str:sign>/', RegisterActivateView.as_view(), name='register_activate'),
    path('<int:pk>/delete_user', DeleteUserView.as_view(), name='delete_user')
]
