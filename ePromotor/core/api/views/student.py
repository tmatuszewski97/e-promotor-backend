from rest_framework import generics, status
from core.api.serializers import student as studentSerializers
from core.api.serializers import file as fileSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsAdministratorOrDeanWorker, IsNotStudent
from rest_framework.response import Response
from core.models import Student, User
from core.my_functions import normalize_string
from django.http import Http404
import io
import csv


# Views associated with User model with student role


class StudentBulkDelete(generics.CreateAPIView):
    serializer_class = studentSerializers.StudentBulkDeleteSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        list_of_ids = []
        for student_data in serializer.validated_data:
            list_of_ids.append(student_data["id"])
        users_to_delete = Student.objects.filter(id__in=list_of_ids)
        if (len(users_to_delete) <= 0):
            return Response({'message': "Couldn't find students to delete", }, status=status.HTTP_400_BAD_REQUEST)
        else:
            users_to_delete.delete()
            return Response({
                'message': "Students successfully deleted"
            })


class StudentBulkRegister(generics.CreateAPIView):
    serializer_class = fileSerializers.FileAddSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        file_extension = str(file).split('.').pop()
        if (file_extension != 'csv'):
            return Response({'message': "Wrong file extension", }, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = file.read().decode('utf-8-sig')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=';')
        students = []
        for i, row in enumerate(reader):
            if i == 0:
                pass
            else:
                if len(row) != 5:
                    return Response({'message': "Wrong file structure", }, status=status.HTTP_400_BAD_REQUEST)
                fn_wo_accents = normalize_string(row[1])
                ln_wo_accents = normalize_string(row[2])
                # Password (without accents) = Sign $ + first 3 letters of name + first 3 letters of surname + last 3 numbers from index
                password = '$'+fn_wo_accents[0:3] + \
                    ln_wo_accents[0:3]+row[0][3:6]
                obj = {
                    'user': {
                        'email': row[0]+'@uwm.pl',
                        'first_name': row[1],
                        'last_name': row[2],
                        'password': password,
                        'password2': password
                    },
                    'index': row[0],
                    'cycle_degree': row[3],
                    'specialization': row[4]
                }
                student = studentSerializers.StudentRegisterSerializer(
                    data=obj)
                student.is_valid(raise_exception=True)
                students.append(obj)

        if (i == len(students)):
            for studentData in students:
                student = studentSerializers.StudentRegisterSerializer(
                    data=studentData)
                student.is_valid(raise_exception=False)
                student.save()
            return Response({
                'message': "Students successfully registered"
            })


class StudentRegister(generics.CreateAPIView):
    serializer_class = studentSerializers.StudentRegisterSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': "Successfully registered a student",
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
        })


class StudentList(generics.ListAPIView):
    serializer_class = studentSerializers.StudentUserListSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]
    queryset = Student.objects.all().order_by(
        'user__first_name', 'user__last_name')


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = studentSerializers.StudentUserDetailSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]
    queryset = Student.objects.all()
