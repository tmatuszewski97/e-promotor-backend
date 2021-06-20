from rest_framework import serializers
from core.models import Student
from core.api.serializers import user as userSerializers
from .choice_field import ChoiceField


# Serializers for Student model


class StudentBulkDeleteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ['id']
        extra_kwargs = {
            'id': {'write_only': True, 'required': True},
        }


class StudentRegisterSerializer(serializers.ModelSerializer):
    user = userSerializers.UserRegisterSerializer()
    cycle_degree = ChoiceField(choices=Student.CYCLE_DEGREE_CHOICES)

    class Meta:
        model = Student
        fields = ['user', 'id', 'index', 'cycle_degree', 'specialization']
        extra_kwargs = {
            'user': {'required': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = userSerializers.UserRegisterSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save(new_role=4, is_staff=False)
        student_instance = Student.objects.create(
            user=user_instance, **validated_data)
        return user_instance


class StudentUserListSerializer(serializers.ModelSerializer):
    user = userSerializers.UserListSerializer()
    cycle_degree = ChoiceField(choices=Student.CYCLE_DEGREE_CHOICES)

    class Meta:
        model = Student
        fields = ['user', 'id', 'index', 'cycle_degree', 'specialization']
        extra_kwargs = {
            'index': {'read_only': True},
            'cycle_degree': {'read_only': True},
            'specialization': {'read_only': True},
        }


class StudentUserDetailSerializer(serializers.ModelSerializer):
    user = userSerializers.UserDetailForAdminAndDeanWorkerSerializer()
    cycle_degree = ChoiceField(choices=Student.CYCLE_DEGREE_CHOICES)

    class Meta:
        model = Student
        fields = ['user', 'id', 'index', 'cycle_degree', 'specialization']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.index = validated_data.get('index', instance.index)
        instance.cycle_degree = validated_data.get(
            'cycle_degree', instance.cycle_degree)
        instance.specialization = validated_data.get(
            'specialization', instance.specialization)
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
