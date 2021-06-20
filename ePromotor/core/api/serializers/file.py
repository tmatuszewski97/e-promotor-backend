from rest_framework import serializers
from core.models import File
from core.api.serializers import user as userSerializers
from .choice_field import ChoiceField

# Serializers for File model


class FileForGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file']
        extra_kwargs = {
            'file': {'read_only': True},
        }


class FileAddSerializer(serializers.ModelSerializer):
    shared_for = ChoiceField(choices=File.ROLE_CHOICES, required=False)

    class Meta:
        model = File
        fields = ['id', 'file', 'shared_for']


class FileUserForGetSerializer(serializers.ModelSerializer):
    creator = userSerializers.UserListSerializer()
    shared_for = ChoiceField(choices=File.ROLE_CHOICES)

    class Meta:
        model = File
        fields = ['id', 'file', 'shared_for', 'creation_date', 'creator']
        extra_kwargs = {
            'file': {'read_only': True},
            'shared_for': {'read_only': True},
            'creation_date': {'read_only': True},
        }


class FileUserForUpdateSerializer(serializers.ModelSerializer):
    shared_for = ChoiceField(choices=File.ROLE_CHOICES)

    class Meta:
        model = File
        fields = ['id', 'shared_for']
