from django.urls import path
from . views import ListCustomUsersApiView, CreateCustomUserApiView, CustomTokenObtainPairView, CreateGroupApiView, ListGroupsApiView \
, RetrieveUpdateDestroyCustomUserApiView, RetrieveUpdateDestroyGroupApiView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register', CreateCustomUserApiView.as_view(), name='signup'),
    path('login', CustomTokenObtainPairView.as_view(), name='signin'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('users', ListCustomUsersApiView.as_view(), name='list-users'),
    path('users/<int:pk>', RetrieveUpdateDestroyCustomUserApiView.as_view(), name='user-detail'),
    path('groups/create', CreateGroupApiView.as_view(), name='create-group'),
    path('groups', ListGroupsApiView.as_view(), name='list-groups'),
    path('groups/<int:pk>', RetrieveUpdateDestroyGroupApiView.as_view(), name='group-detail'),
]