from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, GroupSerializer, CreateGroupSerializer \
    , CategorySerializer, CreateCategorySerializer, SupplierSerializer, CreateSupplierSerializer, GroupQueueSerializer, GroupTaskSerializer \
    , UserDataSerializer, SupplierNameSerializer, AuditLogSerializer, SupplierViewsetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.authentication import EmailLoginBackend
from drf_spectacular.utils import extend_schema
from users.models import CustomUser, AuditLog
from rest_framework_simplejwt.tokens import RefreshToken
from groups.models import Group, GroupTask, GroupQueue
from items.models import Category, Supplier
from rest_framework.views import APIView
from . permissions import IsOwner, IsSuperUser


class PasswordlessLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        user = self.authenticate(username)

        if user is None:
            return Response({'error': 'Invalid username'}, status=401)

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)
        email = user.email

        return Response({'refresh': refresh, 'access': access, 'email': email})

    def authenticate(self, username):
        # Use your custom backend logic here (defined in step 1)
        return EmailLoginBackend().authenticate(self.request, username)

class CreateCustomUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class ListCustomUsersApiView(ListAPIView):
    serializer_class = ListCustomUserSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = [IsAuthenticated, IsSuperUser]
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyCustomUserApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDataSerializer(user, data=request.data, partial=True)
        # if exception is raised then return 400 with a detail message
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ListGroupsApiView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]


class CreateGroupApiView(CreateAPIView):
    serializer_class = CreateGroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    

class RetrieveUpdateDestroyGroupApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = CreateGroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ListCategoriesApiView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]


class CreateCategoryApiView(CreateAPIView):
    serializer_class = CreateCategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RetrieveUpdateDestroyCategoryApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ListCreateSuppliersApiView(ListCreateAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = []


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')  # Access specific query param
        if name:
            queryset = queryset.filter(name__icontains=name)  # Filter by name (case-insensitive)
        return queryset
    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierNameSerializer
        return super().get_serializer_class()
    

    @extend_schema(responses={200: SupplierSerializer}, description="This is a get request to get list of all suppliers")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
        

class RetrieveUpdateDestroySupplierApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = []

    def get(self, request, *args, **kwargs):
        supplier = self.get_object()
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        supplier = self.get_object()
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        supplier = self.get_object()
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierViewsetSerializer
    queryset = Supplier.objects.all()
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace', 'delete',]
    permission_classes = []

    def destroy(self, request, pk=None):
        return super().destroy(request, pk)
    

class ListGroupsTasksApiView(ListAPIView):
    serializer_class = GroupTaskSerializer
    queryset = GroupTask.objects.all()
    permission_classes = [IsAuthenticated]


class ListGroupsQueueApiView(ListAPIView):
    serializer_class = GroupQueueSerializer
    queryset = GroupQueue.objects.all()
    permission_classes = [IsAuthenticated]


class MyGroupTasksApiListView(ListAPIView):
    serializer_class = GroupTaskSerializer
    model = GroupTask
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupTask.objects.filter(user=self.request.user)
    
    
class MyGroupQueueApiListView(ListAPIView):
    serializer_class = GroupQueueSerializer
    model = GroupQueue
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupQueue.objects.filter(created_by=self.request.user)
    

class UpdateGroupTaskApiView(RetrieveUpdateAPIView):
    serializer_class = GroupTaskSerializer
    queryset = GroupTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # raise forbidden if user is not the owner of the task
        group_task = self.get_object()
        if group_task.user != request.user:
            return Response(data={"detail": "You are not the owner of this task."}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)
    

class ListAuditLogsApiView(ListAPIView):
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]
    
    def get_queryset(self):
        return AuditLog.objects.filter(created_by=self.request.user)
    
    
    


    

