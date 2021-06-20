from rest_framework import serializers
from core.models import Promoter
from core.api.serializers import user as userSerializers
from .choice_field import ChoiceField


# Serializers for Promoter model


class PromoterBulkDeleteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Promoter
        fields = ['id']
        extra_kwargs = {
            'id': {'write_only': True, 'required': True},
        }


class PromoterRegisterSerializer(serializers.ModelSerializer):
    user = userSerializers.UserRegisterSerializer()
    title = ChoiceField(choices=Promoter.TITLE_CHOICES)

    class Meta:
        model = Promoter
        fields = ['user', 'id', 'title', 'image', 'proposed_topics',
                  'unwanted_topics', 'interests', 'contact', 'max_students_number']
        extra_kwargs = {
            'user': {'required': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = userSerializers.UserRegisterSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save(new_role=3, is_staff=False)
        promoter_instance = Promoter.objects.create(
            user=user_instance, **validated_data)
        return user_instance


class PromoterUserListSerializer(serializers.ModelSerializer):
    user = userSerializers.UserListSerializer()
    title = ChoiceField(choices=Promoter.TITLE_CHOICES)

    class Meta:
        model = Promoter
        fields = ['user', 'id', 'title', 'image']
        extra_kwargs = {
            'title': {'read_only': True},
            'image': {'read_only': True},
        }


class PromoterUserDetailForAdminAndDeanWorkerSerializer(serializers.ModelSerializer):
    user = userSerializers.UserDetailForAdminAndDeanWorkerSerializer()
    title = ChoiceField(choices=Promoter.TITLE_CHOICES)

    class Meta:
        model = Promoter
        fields = ['user', 'id', 'title', 'image', 'proposed_topics',
                  'unwanted_topics', 'interests', 'contact', 'max_students_number']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.proposed_topics = validated_data.get(
            'proposed_topics', instance.proposed_topics)
        instance.unwanted_topics = validated_data.get(
            'unwanted_topics', instance.unwanted_topics)
        instance.interests = validated_data.get(
            'interests', instance.interests)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.max_students_number = validated_data.get(
            'max_students_number', instance.max_students_number)
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


class PromoterUserDetailSerializer(serializers.ModelSerializer):
    user = userSerializers.UserDetailForPromoterSerializer()
    title = ChoiceField(choices=Promoter.TITLE_CHOICES)

    class Meta:
        model = Promoter
        fields = ['user', 'id', 'title', 'image', 'proposed_topics',
                  'unwanted_topics', 'interests', 'contact', 'max_students_number']
        extra_kwargs = {
            'max_students_number': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.proposed_topics = validated_data.get(
            'proposed_topics', instance.proposed_topics)
        instance.unwanted_topics = validated_data.get(
            'unwanted_topics', instance.unwanted_topics)
        instance.interests = validated_data.get(
            'interests', instance.interests)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.max_students_number = validated_data.get(
            'max_students_number', instance.max_students_number)
        instance.save()

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        return instance


class PromoterUserDetailWithFilesSerializer(serializers.ModelSerializer):
    user = userSerializers.UserDetailWithFilesSerializer()
    title = ChoiceField(choices=Promoter.TITLE_CHOICES)

    class Meta:
        model = Promoter
        fields = ['user', 'id', 'title', 'image', 'proposed_topics',
                  'unwanted_topics', 'interests', 'contact', 'max_students_number']
        extra_kwargs = {
            'max_students_number': {'read_only': True},
        }
