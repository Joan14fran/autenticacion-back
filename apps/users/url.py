from django.urls import path
from apps.users.views import *

urlpatterns = [
    path('api/signin/', SignIn.as_view(), name='signin'),
    path('api/signup/', SignUp.as_view(), name='signup'),
]
