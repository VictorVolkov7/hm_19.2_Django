from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, VerifiedSentView, verify_email, ProfileView, \
    generate_new_password

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/verified_sent/', VerifiedSentView.as_view(), name='verified_sent'),
    path('verify_email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
]
