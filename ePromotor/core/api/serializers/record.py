from rest_framework import serializers
from core.models import Record, Student
from core.api.serializers import promoter as promoterSerializers
from core.api.serializers import student as studentSerializers
from core.my_functions import are_elections_ended, are_requests_sent


# Serializers for Record model


class GetElectionsStatusSerializer(serializers.ModelSerializer):
    elections_ended = serializers.SerializerMethodField(read_only=True)
    students_in_numbers = serializers.SerializerMethodField(read_only=True)
    requests_sent = serializers.SerializerMethodField(read_only=True)
    tour_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Record
        fields = ['students_in_numbers', 'elections_ended',
                  'requests_sent', 'tour_number']

    def get_students_in_numbers(self, obj):
        records = Record.objects.all()
        all_students = Student.objects.all()
        disqualified_students = []
        chosen_students = []
        for record in records:
            if (record.was_revoked == True and record.student not in disqualified_students):
                disqualified_students.append(record.student)
            elif (record.was_selected == True and record.student not in chosen_students):
                chosen_students.append(record.student)
        response = {
            'all_students': all_students.count(),
            'disqualified_students': len(disqualified_students),
            'chosen_students': len(chosen_students)
        }
        return response

    def get_elections_ended(self, obj):
        return are_elections_ended()

    def get_requests_sent(self, obj):
        return are_requests_sent()

    def get_tour_number(self, obj):
        return Record.objects.order_by('-tour_number').first().tour_number


class RecordPromoterStudentListSerializer(serializers.ModelSerializer):
    promoter = promoterSerializers.PromoterUserListSerializer(read_only=True)
    student = studentSerializers.StudentUserListSerializer(read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'tour_number', 'preference_number',
                  'academic_year', 'was_revoked', 'was_sent', 'was_selected', 'promoter', 'student']
        extra_kwargs = {
            'tour_number': {'read_only': True},
            'preference_number': {'read_only': True},
            'academic_year': {'read_only': True},
            'was_revoked': {'read_only': True},
            'was_sent': {'read_only': True},
            'was_selected': {'read_only': True},
        }


class RecordPromoterStudentDetailForPromoterSerializer(serializers.ModelSerializer):
    promoter = promoterSerializers.PromoterUserDetailSerializer(read_only=True)
    student = studentSerializers.StudentUserDetailSerializer(read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'tour_number', 'preference_number',
                  'academic_year', 'was_revoked', 'was_sent', 'was_selected', 'promoter', 'student']
        extra_kwargs = {
            'tour_number': {'read_only': True},
            'preference_number': {'read_only': True},
            'academic_year': {'read_only': True},
            'was_revoked': {'read_only': True},
            'was_sent': {'read_only': True},
            'was_selected': {'required': True},
        }


class RecordPromoterStudentDetailForStudentSerializer(serializers.ModelSerializer):
    promoter = promoterSerializers.PromoterUserDetailSerializer(
        allow_null=True)
    student = studentSerializers.StudentUserDetailSerializer(read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'tour_number', 'preference_number',
                  'academic_year', 'was_revoked', 'was_sent', 'was_selected', 'promoter', 'student']
        extra_kwargs = {
            'tour_number': {'read_only': True},
            'preference_number': {'read_only': True},
            'academic_year': {'read_only': True},
            'was_revoked': {'read_only': True},
            'was_sent': {'read_only': True},
            'was_selected': {'read_only': True},
        }
