from rest_framework import serializers
from users.models import CustomUser, AuditLog
from django.dispatch import Signal
from groups.models import Group, GroupQueue, GroupTask
from items.models import Category, Supplier
# use @extend_schema_field to add custom description to the field
from drf_spectacular.utils import extend_schema_field
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . handlers import create_supplier_handler
from . signals import create_supplier_signal


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
    
    @extend_schema_field(serializers.CharField)
    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    @extend_schema_field(serializers.CharField)
    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token),
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserDataSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(max_length=None, use_url=True, required=False)
    # example for related name group created
    # groups_created = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'profile_image', 'is_staff', 'role', 'is_superuser',)
    
    def validate_profile_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size should not exceed 1MB')
        return value


class ListCustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'role', 'is_superuser',)


class GroupSerializer(serializers.ModelSerializer):

    moderator = CustomUserSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):

    moderator = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())

    class Meta:
        model = Group
        read_only_fields = ('created_by', 'created_at', 'updated_at')
        fields = ('name', 'description', 'created_by', 'moderator', 'created_at', 'updated_at')
    

class CategorySerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='created_by.email', read_only=True)
    
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

    def create(self, validated_data):
        supplier = super(SupplierSerializer, self).create(validated_data)
        supplier.save()
    
        # Send a signal that a new supplier has been created
        create_supplier_signal.connect(create_supplier_handler, sender=Supplier)
        create_supplier_signal.send(sender=self.__class__, supplier_instance=supplier)
        return supplier
    

class SupplierViewsetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'

    def create(self, validated_data):
        supplier = super(SupplierSerializer, self).create(validated_data)
        supplier.save()
        return supplier


class SupplierNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ('name', 'json_data',)


class CreateSupplierSerializer(serializers.ModelSerializer):

    nickname = serializers.CharField(max_length=100, required=False, write_only=True)
    
    class Meta:
        model = Supplier
        read_only_fields = ('created_at', 'updated_at',)
        fields = ('name', 'created_at', 'updated_at', 'nickname')

        
    def create(self, validated_data):
        print('Validated data ', validated_data)
        # pop the nickname from the validated data
        nickname = validated_data.pop('nickname', None)
        supplier = super(CreateSupplierSerializer, self).create(validated_data)
        supplier.save()
    
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

    @extend_schema_field(serializers.CharField)
    def get_group_name(self, obj):
        return obj.group_queue.group.name
    
    @extend_schema_field(serializers.CharField)
    def get_user_name(self, obj):
        if obj.user.username:
            return obj.user.username
        else:
            return obj.user.email


class GroupQueueSerializer(serializers.ModelSerializer):

    group_name = serializers.SerializerMethodField()
    group_created_by = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    moderator_approved = serializers.SerializerMethodField()

    class Meta:
        model = GroupQueue
        fields = '__all__'

    @extend_schema_field(serializers.CharField)
    def get_group_name(self, obj):
        return obj.group.name
    
    @extend_schema_field(serializers.CharField)
    def get_group_created_by(self, obj):
        if obj.created_by.username:
            return obj.created_by.username
        else:
            return obj.created_by.email
    
    @extend_schema_field(GroupTaskSerializer)
    def get_tasks(self, obj):
        tasks = GroupTask.objects.filter(group_queue=obj)
        return GroupTaskSerializer(tasks, many=True).data
    
    @extend_schema_field(serializers.BooleanField)
    def get_moderator_approved(self, obj):
        # check if any of the tasks in the queue has been approved by the moderator
        
        for task in obj.group_task.all():
            if task.status and not task.user.is_superuser:
                return True
        return False
    

class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditLog
        fields = '__all__'