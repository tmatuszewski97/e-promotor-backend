from rest_framework import serializers
from core.models import User, File
from django.core.validators import EmailValidator
from rest_framework.authtoken.models import Token


# Serializers for User model


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                  'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True, 'required': True},
            'role': {'read_only': True},
        }

    def save(self, new_role, is_staff):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            role=new_role,
            staff=is_staff
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']
        extra_kwargs = {
            'old_password': {'write_only': True, 'required': True},
            'password': {'write_only': True, 'required': True},
            'password2': {'write_only': True, 'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is not correct')
        return value


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'email': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'role': {'read_only': True},
        }


class UserDetailForAdminAndDeanWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role',
                  'date_joined', 'last_login', 'active']
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]},
            'role': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'active': {},
        }

    def get_extra_kwargs(self):
        extra_kwargs = super(
            UserDetailForAdminAndDeanWorkerSerializer, self).get_extra_kwargs()
        user = self.context['request'].user

        # Only User with administrator role is able to change 'active' field
        if user.role != 1:
            kwargs = extra_kwargs.get('active', {})
            kwargs['read_only'] = True
            extra_kwargs['active'] = kwargs

        return extra_kwargs


class UserDetailForPromoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role',
                  'date_joined', 'last_login', 'active']
        extra_kwargs = {
            'email': {'read_only': True},
            'role': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'active': {},
        }


class UserDetailWithFilesSerializer(serializers.ModelSerializer):

    def get_filtered_files(self, user):
        request = self.context.get("request")
        logged_user = request.user
        if logged_user.role != 1:
            queryset = File.objects.filter(
                shared_for=logged_user.role, creator=user)
        else:
            queryset = File.objects.filter(creator=user)
         # Local import to win with circular dependencies error
        from core.api.serializers.file import FileForGetSerializer
        serializer = FileForGetSerializer(
            instance=queryset, many=True, context={"request": request})
        return serializer.data

    files = serializers.SerializerMethodField('get_filtered_files')

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role',
                  'date_joined', 'last_login', 'active', 'files']
        extra_kwargs = {
            'email': {'read_only': True},
            'role': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'active': {},
        }
