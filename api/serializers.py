from rest_framework import serializers
from users.models import CustomUser
from groups.models import Group, GroupQueue, GroupTask
from items.models import Category, Supplier
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('No account exists with these credentials, check password and email')
    }

    def validate(self, attrs):
        
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data 
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['id'] = self.user.id
        data['is_admin'] = self.user.is_superuser
        data['role'] = self.user.role
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        min_length=8,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'password', 'access', 'refresh', 'role', 'is_superuser',)
    
    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token),
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListCustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'role', 'is_superuser',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        read_only_fields = ('created_by', 'created_at', 'updated_at')
        fields = ('name', 'description', 'created_by', 'created_at', 'updated_at')
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        read_only_fields = ('created_by', 'created_at', 'updated_at')
        fields = ('name', 'created_by', 'created_at', 'updated_at')

    
    def create(self, validated_data):
        category = super(CreateCategorySerializer, self).create(validated_data)
        category.save()
        return category
    
    def update(self, instance, validated_data):
        category = super(CreateCategorySerializer, self).update(instance, validated_data)
        category.save()
        return category
    

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'


class CreateSupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        read_only_fields = ('created_at', 'updated_at')
        fields = ('name', 'created_at', 'updated_at')

        
        def create(self, validated_data):
            supplier = super(CreateSupplierSerializer, self).create(validated_data)
            supplier.save()
            return supplier
        
        def update(self, instance, validated_data):
            supplier = super(CreateSupplierSerializer, self).update(instance, validated_data)
            supplier.save()
            return supplier
        

class GroupTaskSerializer(serializers.ModelSerializer):

    group_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = GroupTask
        fields = '__all__'

    def get_group_name(self, obj):
        return obj.group_queue.group.name
    
    def get_user_name(self, obj):
        if obj.user.username:
            return obj.user.username
        else:
            return obj.user.email


class GroupQueueSerializer(serializers.ModelSerializer):

    group_name = serializers.SerializerMethodField()
    group_created_by = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = GroupQueue
        fields = '__all__'

    def get_group_name(self, obj):
        return obj.group.name
    
    def get_group_created_by(self, obj):
        if obj.created_by.username:
            return obj.created_by.username
        else:
            return obj.created_by.email
    
    def get_tasks(self, obj):
        tasks = GroupTask.objects.filter(group_queue=obj)
        return GroupTaskSerializer(tasks, many=True).data
    