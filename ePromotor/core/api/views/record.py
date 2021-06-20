from rest_framework import generics, status
from django.conf import settings
from django.core.files.base import File as FileBase
from core.api.serializers import record as recordSerializer
from core.api.serializers import file as fileSerializers
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdministratorOrDeanWorker, IsPromoter, IsStudent, IsPromoterOfRecord, IsStudentOfRecordFromUrl
from rest_framework.response import Response
from core.models import File, Promoter, Student, Record
from django.db.models.query_utils import Q
from core.my_functions import are_elections_ended, have_free_place, get_actual_tour_number, found_promoter, found_another_promoter, are_requests_sent, get_actual_preference_number, was_disqualified, should_start_a_new_tour, create_records_for_new_tour
from django.http import Http404
import csv
import os


# Views associated with Record model


class GetElectionsStatus(generics.RetrieveAPIView):
    serializer_class = recordSerializer.GetElectionsStatusSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]

    def get_object(self):
        record = Record.objects.first()
        if (record is None):
            raise Http404
        else:
            return record


class RecordListForPromoter(generics.ListAPIView):
    serializer_class = recordSerializer.RecordPromoterStudentListSerializer
    permission_classes = (IsAuthenticated & IsPromoter,)
    # permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        promoter = Promoter.objects.get(user=user)
        if (are_requests_sent() is False):
            return Record.objects.filter(promoter=promoter, was_selected=True)
        # Only if every student sent requests to promoters (was_sent==True), promoters will be able to see their applications
        else:
            actual_preference_number = get_actual_preference_number()
            # If there is no waiting requests for logged promoter, show selected students (was_selected=True)
            if actual_preference_number == 0:
                return Record.objects.filter(promoter=promoter, was_selected=True)
            # If there are some requests waiting for promoters decisions, show them in order (smaller preference_number will be shown earlier)
            else:
                if (actual_preference_number == 1):
                    all_requests = Record.objects.filter(
                        promoter=promoter, preference_number=actual_preference_number, was_revoked=False, was_sent=True)
                elif (actual_preference_number == 2):
                    all_requests = Record.objects.filter(
                        Q(promoter=promoter) & ~Q(preference_number=3) & Q(was_revoked=False) & Q(was_sent=True))
                else:
                    all_requests = Record.objects.filter(
                        Q(promoter=promoter) & Q(was_revoked=False) & Q(was_sent=True))
                queryset = all_requests
                for request in all_requests:
                    if ((found_another_promoter(promoter=promoter, student=request.student) is True) or (request.was_selected is False)):
                        print(request)
                        queryset = queryset.exclude(id=request.id)
                return queryset


class RecordDetailForPromoter(generics.RetrieveUpdateAPIView):
    serializer_class = recordSerializer.RecordPromoterStudentDetailForPromoterSerializer
    permission_classes = (IsAuthenticated & IsPromoter & IsPromoterOfRecord,)
    # permission_classes = [AllowAny]

    def get_object(self):
        user = self.request.user
        promoter = Promoter.objects.get(user=user)
        record_id = self.kwargs.get('pk')
        if (are_requests_sent() is False):
            return Record.objects.get(pk=record_id, promoter=promoter, was_selected=True)
        else:
            actual_preference_number = get_actual_preference_number()
            try:
                record = Record.objects.get(
                    pk=record_id, promoter=promoter, preference_number=actual_preference_number, was_revoked=False, was_sent=True)
            except Record.DoesNotExist:
                raise Http404
            else:
                return record

    def put(self, request, *args, **kwargs):
        record = self.get_object()
        user = self.request.user
        promoter = Promoter.objects.get(user=user)
        if (record.was_selected != None):
            return Response({
                'message': "You can't change your decision",
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if ((have_free_place(promoter=promoter) is False) and (serializer.validated_data['was_selected'] is True)):
            return Response({
                'message': "You can't take more students",
            }, status=status.HTTP_400_BAD_REQUEST)
        record.was_selected = serializer.validated_data['was_selected']
        record.save()

        if (serializer.validated_data['was_selected'] is True):
            # If student was selected by promoter, every other Record from his preferences getting field was_selected as False
            Record.objects.filter(student=record.student, was_revoked=False, was_selected=None).update(
                was_selected=False)
            # Also check, if promoter got maximum number of students, every other request which was sent to him getting status: was_selected=False
            if (have_free_place(promoter=promoter) is False):
                Record.objects.filter(promoter=promoter, was_revoked=False, was_selected=None).update(
                    was_selected=False)
                # If there is no waiting requests (was_selected != None), and some students still not found a promoter, we create new records for next tour
                if (should_start_a_new_tour() is True):
                    create_records_for_new_tour()
            return Response({
                'message': "Successfully accepted a student request",
            })
        else:
            # What will be done, if promoter doesn't accept a student request
            if (should_start_a_new_tour() is True):
                create_records_for_new_tour()
            return Response({
                'message': "Successfully rejected a student request"
            })


class RecordListForStudent(generics.ListCreateAPIView):
    serializer_class = recordSerializer.RecordPromoterStudentListSerializer
    permission_classes = (IsAuthenticated & IsStudent,)
    # permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(user=user)

        # If student found promoter, he see the informations about this tour
        try:
            was_selected_record = Record.objects.get(
                student=student, was_selected=True)
        # If student is still searching Promoter, he is able to see the informations about actual tour (3 records in each tour)
        except Record.DoesNotExist:
            if (was_disqualified(student)):
                return Record.objects.filter(student=student).order_by('-tour_number')
            else:
                actual_tour_number = get_actual_tour_number()
                return Record.objects.filter(student=student, tour_number=actual_tour_number).order_by('preference_number')
        else:
            return Record.objects.filter(student=student, tour_number=was_selected_record.tour_number).order_by('preference_number')

    def post(self, request, *args, **kwargs):
        user = self.request.user
        student = Student.objects.get(user=user)

        actual_tour_number = get_actual_tour_number()
        records_to_send = Record.objects.filter(
            student=student, tour_number=actual_tour_number)

        if (found_promoter(student=student) is True):
            return Response({
                'message': "You have already found a promoter",
            }, status=status.HTTP_400_BAD_REQUEST)

        elif (was_disqualified(student=student) is True):
            return Response({
                'message': "You have been disqualified from elections",
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            for record in records_to_send:
                if (record.promoter is None):
                    return Response({
                        'message': "You didn't defined promoter for every preference",
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif (record.was_sent is True):
                    return Response({
                        'message': "You have already sent requests to promoters in this tour",
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif (have_free_place(record.promoter) is False):
                    record.promoter = None
                    record.save()
                    return Response({
                        'message': "One promoter from your preferences hasn't got free place for new student",
                    }, status=status.HTTP_400_BAD_REQUEST)

            # If everyting was fine - mark records as sent
            records_to_send.update(was_sent=True)
            return Response({
                'message': "Your requests have been sent to promoters",
            })


class RecordDetailForStudent(generics.UpdateAPIView):
    serializer_class = recordSerializer.RecordPromoterStudentDetailForStudentSerializer
    permission_classes = (IsAuthenticated & IsStudent &
                          IsStudentOfRecordFromUrl,)
    # permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        record_id = self.kwargs.get('pk')
        record = Record.objects.get(pk=record_id)
        if (record.was_revoked == True):
            return Response({'message': "You can't make any actions with records when you are disqualified", }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if (serializer.validated_data['promoter'] != None):
            return Response({'message': "You can only delete promoter chosen on preference", }, status=status.HTTP_400_BAD_REQUEST)
        record.promoter = serializer.validated_data['promoter']
        record.save()
        return Response({
            'message': "Successfully updated a record"
        })


class RecordListSummary(generics.ListAPIView):
    serializer_class = recordSerializer.RecordPromoterStudentListSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def get_queryset(self):
        return Record.objects.filter(Q(was_selected=True) | Q(was_revoked=True)).order_by('was_selected')


class RevokeRecords(generics.UpdateAPIView):
    serializer_class = recordSerializer.RecordPromoterStudentListSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        if (are_elections_ended()):
            return Response({'message': "You can't revoke records when elections are ended", }, status=status.HTTP_400_BAD_REQUEST)
        actual_tour_number = get_actual_tour_number()
        not_sent_records = Record.objects.filter(
            tour_number=actual_tour_number, was_sent=False)
        if (not_sent_records.filter(was_revoked=True).count() > 0):
            return Response({'message': "You have already revoked records in this tour", }, status=status.HTTP_400_BAD_REQUEST)
        else:
            students = []
            for record in not_sent_records:
                if (record.student not in students):
                    students.append(record.student)
                else:
                    not_sent_records = not_sent_records.exclude(id=record.id)
                    record.delete()

            not_sent_records.update(was_revoked=True, promoter=None)
            return Response({'message': "Successfully revoked records in this tour"})


class RecordListSummaryToCsvFile(generics.RetrieveAPIView):
    serializer_class = fileSerializers.FileAddSerializer
    permission_classes = (IsAuthenticated & IsAdministratorOrDeanWorker,)
    # permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        records_to_save = Record.objects.filter(
            Q(was_selected=True) | Q(was_revoked=True)).order_by('was_selected')
        if len(records_to_save) <= 0:
            return Response({'message': "Couldn't export empty data to file", }, status=status.HTTP_400_BAD_REQUEST)
        filename = 'tmp.csv'
        new_filename = 'lista_wynikowa.csv'
        if settings.DEBUG is True:
            path = os.path.join(settings.MEDIA_ROOT, 'files', filename)
        else:
            path = filename
        with open(path, "w", encoding="utf-8", newline='') as f:
            f.write('\ufeff')
            header = ['student', 'indeks', 'stopień',
                      'specjalizacja', 'promotor']
            csv_writer = csv.DictWriter(
                f, fieldnames=header, delimiter=';', lineterminator='\n', dialect='excel')
            csv_writer.writeheader()

            for record in records_to_save:
                promoter_data = ''
                cycle_degree = ''

                if record.promoter != None:
                    promoter_data = record.promoter.user.first_name + \
                        " " + record.promoter.user.last_name
                else:
                    promoter_data = 'niewybrany'

                if record.student.cycle_degree == 1:
                    cycle_degree = 'pierwszy'
                elif record.student.cycle_degree == 2:
                    cycle_degree = 'drugi'
                else:
                    cycle_degree = ''

                csv_writer.writerow({
                    'student': record.student.user.first_name + " " + record.student.user.last_name,
                    'indeks': record.student.index,
                    'stopień': cycle_degree,
                    'specjalizacja': record.student.specialization,
                    'promotor': promoter_data
                })
        f.close()

        with open(path, 'rb') as fi:
            file_instance = File(creator=self.request.user)
            file_instance.file.save(new_filename, FileBase(fi))
            file_instance.save()
        fi.close()

        if settings.DEBUG is True:
            os.remove(path)

        return Response({
            'message': "Successfully exported a .csv file",
        })
