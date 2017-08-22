from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserUpdateAPIView,
    UserDetailAPIView
    )

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    #url(r'^login/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'^details/$',UserDetailAPIView.as_view(),name='detail'),
    url(r'^update/(?P<pk>\d+)/$',UserUpdateAPIView.as_view(),name='update'),
]