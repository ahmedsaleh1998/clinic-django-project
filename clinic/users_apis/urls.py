from django.urls import path
from .views import ActivateUser, Login, Logout, Register

app_name='users_apis'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('<int:pk>/<str:token>', ActivateUser.as_view(), name='activate_user'),

]
