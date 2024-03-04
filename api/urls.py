from django.urls import path
from . views import ListCustomUsersApiView, CreateCustomUserApiView, CustomTokenObtainPairView, CreateGroupApiView, ListGroupsApiView \
, RetrieveUpdateDestroyCustomUserApiView, RetrieveUpdateDestroyGroupApiView, ListSuppliersApiView \
, CreateSupplierApiView, RetrieveUpdateDestroySupplierApiView, ListCategoriesApiView, CreateCategoryApiView, RetrieveUpdateDestroyCategoryApiView \
, ListGroupsTasksApiView, ListGroupsQueueApiView, MyGroupQueueApiListView, MyGroupTasksApiListView, UpdateGroupTaskApiView

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
    path('suppliers', ListSuppliersApiView.as_view(), name='list-suppliers'),
    path('suppliers/create', CreateSupplierApiView.as_view(), name='create-supplier'),
    path('suppliers/<str:pk>', RetrieveUpdateDestroySupplierApiView.as_view(), name='supplier-detail'),
    path('categories', ListCategoriesApiView.as_view(), name='list-categories'),
    path('categories/create', CreateCategoryApiView.as_view(), name='create-category'),
    path('categories/<str:pk>', RetrieveUpdateDestroyCategoryApiView.as_view(), name='category-detail'),
    path('group-tasks', ListGroupsTasksApiView.as_view(), name='list-group-tasks'),
    path('group-queues', ListGroupsQueueApiView.as_view(), name='list-group-queue'),
    path('my-group-queues', MyGroupQueueApiListView.as_view(), name='my-group-queues'),
    path('my-group-tasks', MyGroupTasksApiListView.as_view(), name='my-group-tasks'),
    path('group-tasks/<int:pk>', UpdateGroupTaskApiView.as_view(), name='update-group-task')
]