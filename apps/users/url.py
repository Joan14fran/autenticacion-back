from django.urls import path, include
from apps.users.views import *

urlpatterns = [
    path('api/signin/', SignIn.as_view(), name='signin'),
    path('api/signup/', SignUp.as_view(), name='signup'),
    path('api/logout/', Logout.as_view(), name='logout'),
    # NEW: custom verify-token view which is not included in django-rest-passwordreset
    # path('reset-password/verify-token/', CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    # NEW: The django-rest-passwordreset urls to request a token and confirm pw-reset
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
