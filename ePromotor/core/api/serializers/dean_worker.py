from rest_framework import serializers
from core.models import DeanWorker
from core.api.serializers import user as userSerializers


# Serializers for DeanWorker model


class DeanWorkerRegisterSerializer(serializers.ModelSerializer):
    user = userSerializers.UserRegisterSerializer()

    class Meta:
        model = DeanWorker
        fields = ['user', 'id', 'contact']
        extra_kwargs = {
            'user': {'required': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = userSerializers.UserRegisterSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save(new_role=2, is_staff=False)
        dean_worker_instance = DeanWorker.objects.create(
            user=user_instance, **validated_data)
        return user_instance


class DeanWorkerUserListSerializer(serializers.ModelSerializer):
    user = userSerializers.UserListSerializer()

    class Meta:
        model = DeanWorker
        fields = ['user', 'id', 'contact']
        extra_kwargs = {
            'contact': {'read_only': True},
        }


class DeanWorkerUserDetailSerializer(serializers.ModelSerializer):
    user = userSerializers.UserDetailForAdminAndDeanWorkerSerializer()

    class Meta:
        model = DeanWorker
        fields = ['user', 'id', 'contact']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.contact = validated_data.get('contact', instance.contact)
        instance.save()

        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        # Only User with administrator role is able to change 'active' field
        logged_user = self.context['request'].user
        if logged_user.role == 1:
            user.active = user_data.get('active', user.active)
        user.save()

        return instance
