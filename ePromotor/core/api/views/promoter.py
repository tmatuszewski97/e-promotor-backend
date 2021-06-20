from rest_framework import generics, mixins, status
from core.api.serializers import promoter as promoterSerializers
from core.api.serializers import file as fileSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsAdministratorOrDeanWorker, IsStudent, IsStudentOfRecordFromUrl
from rest_framework.response import Response
from core.models import Promoter, Student, Record
from django.db.models.query_utils import Q
from core.my_functions import have_free_place, are_assigned_to_themselves, normalize_string
from django.http import Http404
import io
import csv


# Views associated with User model with promoter role


class PromoterBulkDelete(generics.CreateAPIView):
    serializer_class = promoterSerializers.PromoterBulkDeleteSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        list_of_ids = []
        for promoter_data in serializer.validated_data:
            list_of_ids.append(promoter_data["id"])
        users_to_delete = Promoter.objects.filter(id__in=list_of_ids)
        if (len(users_to_delete) <= 0):
            return Response({'message': "Couldn't find promoters to delete", }, status=status.HTTP_400_BAD_REQUEST)
        else:
            users_to_delete.delete()
            return Response({
                'message': "Promoters successfully deleted"
            })


class PromoterBulkRegister(generics.CreateAPIView):
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
        promoters = []
        for i, row in enumerate(reader):
            if i == 0:
                pass
            else:
                if len(row) != 9:
                    return Response({'message': "Wrong file structure", }, status=status.HTTP_400_BAD_REQUEST)
                fn_wo_accents = normalize_string(row[1])
                ln_wo_accents = normalize_string(row[2])
                # Password (without accents) = last name + sign @ + additional chars from first column of file
                password = ln_wo_accents+'@'+row[0]
                try:
                    max_students_number = int(row[4])
                except ValueError:
                    return Response({'message': "Błąd konwersji danych", }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = {
                        'user': {
                            # Email (without accents) = first letter lowercased letter from name + lowercased last name + @uwm.pl
                            'email': fn_wo_accents[0].lower()+ln_wo_accents.lower()+'@uwm.pl',
                            'first_name': row[1],
                            'last_name': row[2],
                            'password': password,
                            'password2': password
                        },
                        'title': row[3],
                        'max_students_number': int(row[4]),
                        'proposed_topics': row[5],
                        'unwanted_topics': row[6],
                        'interests': row[7],
                        'contact': row[8]
                    }
                    promoter = promoterSerializers.PromoterRegisterSerializer(
                        data=obj)
                    promoter.is_valid(raise_exception=True)
                    promoters.append(obj)

        if (i == len(promoters)):
            for promoterData in promoters:
                promoter = promoterSerializers.PromoterRegisterSerializer(
                    data=promoterData)
                promoter.is_valid(raise_exception=False)
                promoter.save()
            return Response({
                'message': "Promoters successfully registered"
            })


class PromoterRegister(generics.CreateAPIView):
    serializer_class = promoterSerializers.PromoterRegisterSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': "Successfully registered a promoter",
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
        })


class PromoterList(generics.ListAPIView):
    serializer_class = promoterSerializers.PromoterUserListSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        # If user is an administrator, he is able to see all promoters (even with User.active=False)
        if (user.role == 1):
            return Promoter.objects.all().order_by('-title', 'user__first_name', 'user__last_name')
        else:
            # If not - user see only promoters, who have active account
            return Promoter.objects.filter(Q(user__active=True)).order_by('-title', 'user__first_name', 'user__last_name')


class PromoterDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return promoterSerializers.PromoterUserDetailWithFilesSerializer
        else:
            return promoterSerializers.PromoterUserDetailForAdminAndDeanWorkerSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Everyone who is logged are able to see promoter details
            return [IsAuthenticated(), ]
        else:
            # Only logged users with administrator, dean_worker role can change informations about specified promoter
            return [IsAuthenticated(), IsAdministratorOrDeanWorker(), ]

    def get_queryset(self):
        user = self.request.user
        # If user is an administrator, he is able to see all promoters (even with User.active=False)
        if (user.role == 1):
            return Promoter.objects.all()
        else:
            # If not - User see only promoters, who have active account
            return Promoter.objects.filter(Q(user__active=True))


class PromoterListForRecord(generics.ListAPIView):
    serializer_class = promoterSerializers.PromoterUserListSerializer
    permission_classes = (IsAuthenticated & IsStudent &
                          IsStudentOfRecordFromUrl,)
    # permission_classes = [AllowAny]

    def get_queryset(self):
        record_id = self.kwargs.get('pk')
        if Record.objects.get(pk=record_id).was_revoked is True:
            raise Http404
        else:
            # Students are able to see only promoters, who have active account, have empty place for new student,
            # and actual student didn't choose them as preference in assigned records
            active_promoters = Promoter.objects.filter(Q(user__active=True))
            queryset = active_promoters
            user = self.request.user
            logged_student = Student.objects.get(user=user)
            for active_promoter in active_promoters:
                if ((have_free_place(promoter=active_promoter) == False) or (are_assigned_to_themselves(active_promoter, logged_student) == True)):
                    queryset = queryset.exclude(id=active_promoter.id)
            return queryset.order_by('-title', 'user__first_name', 'user__last_name')


class PromoterDetailForRecord(mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = promoterSerializers.PromoterUserDetailWithFilesSerializer
    permission_classes = (IsAuthenticated & IsStudent &
                          IsStudentOfRecordFromUrl,)
    # permission_classes = [AllowAny];

    def get_object(self):
        record_id = self.kwargs.get('pk')
        if Record.objects.get(pk=record_id).was_revoked is True:
            raise Http404
        else:
            # Students are able to see only promoters, who have active account, have empty place for new student,
            # and actual student didn't choose them as preference in assigned records
            promoter_id = self.kwargs.get('pk_2')
            user = self.request.user
            student = Student.objects.get(user=user)
            try:
                promoter = Promoter.objects.get(
                    id=promoter_id, user__active=True)
            except Promoter.DoesNotExist:
                raise Http404
            if ((have_free_place(promoter=promoter) == True) and (are_assigned_to_themselves(promoter=promoter, student=student) == False)):
                return promoter
            else:
                raise Http404

    lookup_url_kwarg = 'pk_2'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        record_id = self.kwargs.get('pk')
        promoter_id = self.kwargs.get('pk_2')
        record = Record.objects.get(pk=record_id)
        promoter = Promoter.objects.get(pk=promoter_id)

        user = self.request.user
        student = Student.objects.get(user=user)

        if have_free_place(promoter=promoter) is False:
            return Response({
                'message': "This promoter hasn't got free place for new student",
            }, status=status.HTTP_400_BAD_REQUEST)
        elif (are_assigned_to_themselves(promoter=promoter, student=student) == True):
            return Response({
                'message': "You already chose this promoter in one of your preferences",
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            record.promoter = promoter
            record.save()
            return Response({
                'message': "Successfully added promoter on selected preference number",
            })
