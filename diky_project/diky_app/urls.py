from django.urls import path
from .views import CreateUserView, DeleteUsers, GetUsers, LoginView, CheckLoginStatus, LogoutView

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('delete_users/', DeleteUsers.as_view(), name='delete_users'),
    path('get_users/', GetUsers.as_view(), name='get_users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check_login_status/', CheckLoginStatus.as_view(), name='check_login_status')
]