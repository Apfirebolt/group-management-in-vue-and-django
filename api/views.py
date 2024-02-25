from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from . serializers import ListCustomUserSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, GroupSerializer, CreateGroupSerializer \
    , CategorySerializer, CreateCategorySerializer, SupplierSerializer, CreateSupplierSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser
from groups.models import Group
from items.models import Category, Supplier


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
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyCustomUserApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        groups = Group.objects.filter(moderator=user)
        serializer = CustomUserSerializer(user)
        return Response({'user': serializer.data, 'groups': groups.values()}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
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
        serializer = GroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ListCategoriesApiView(ListAPIView):
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
    

class ListSuppliersApiView(ListAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = []


class CreateSupplierApiView(CreateAPIView):
    serializer_class = CreateSupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = []


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

