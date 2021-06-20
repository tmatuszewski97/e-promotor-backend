from core.models import Record, Student
from django.db.models.query_utils import Q
import unicodedata


# My additional functions to prevent code repeating


# Function for checking are elections ended
def are_elections_ended():
    if (Record.objects.filter(was_revoked=False, was_selected=None).count() > 0):
        return False
    else:
        return True


# Function for checking has promoter got a free place for new student
def have_free_place(promoter):
    was_selected_record_number = Record.objects.filter(
        promoter=promoter, was_selected=True).count()
    if (was_selected_record_number >= promoter.max_students_number):
        return False
    else:
        return True


# Function for getting actual tour number
def get_actual_tour_number():
    actual_tour_number = Record.objects.all().order_by(
        '-tour_number').first().tour_number
    return actual_tour_number


# Function for checking is promoter already assigned to student in any record in actual tour
def are_assigned_to_themselves(promoter, student):
    actual_tour_number = get_actual_tour_number()
    try:
        Record.objects.get(promoter=promoter, student=student,
                           tour_number=actual_tour_number)
    except Record.DoesNotExist:
        return False
    else:
        return True


# Function for checking is student already found a promoter (record.was_selected==True)
def found_promoter(student):
    try:
        Record.objects.get(student=student, was_selected=True)
    except Record.DoesNotExist:
        return False
    else:
        return True


# Function for checking is student already found another promoter
def found_another_promoter(promoter, student):
    try:
        record = Record.objects.get(student=student, was_selected=True)
    except Record.DoesNotExist:
        return False
    else:
        if (record.promoter == promoter):
            return False
        else:
            return True


# Function for checking was every student sent requests to promoters in actual tour
def are_requests_sent():
    not_sent_requests = Record.objects.filter(
        was_revoked=False, was_sent=False).count()
    if (not_sent_requests > 0):
        return False
    else:
        return True


# Function for getting actual preference
def get_actual_preference_number():
    if (Record.objects.filter(was_selected=None, was_revoked=False, preference_number=1).count() > 0):
        return 1
    elif (Record.objects.filter(was_selected=None, was_revoked=False, preference_number=2).count() > 0):
        return 2
    elif (Record.objects.filter(was_selected=None, was_revoked=False, preference_number=3).count() > 0):
        return 3
    else:
        return 0


# Function for checking is student disqualified
def was_disqualified(student):
    if (Record.objects.filter(student=student, was_revoked=True).count() > 0):
        return True
    else:
        return False


# Function for checking should a new tour start
def should_start_a_new_tour():
    not_checked_records = Record.objects.filter(
        was_revoked=False, was_selected=None)
    if (not_checked_records.count()) == 0:
        return True
    else:
        return False


# Function which is useful on starting new tour of elections, it creates 3 records for each student who still searching for promoter
def create_records_for_new_tour():
    actual_tour_number = get_actual_tour_number()
    new_tour_number = actual_tour_number+1
    all_students = Student.objects.all()
    free_students = []
    for stud in all_students:
        if ((found_promoter(stud) is False) and (was_disqualified(stud) is False)):
            free_students.append(stud)
    for stud in free_students:
        for i in range(1, 4):
            Record.objects.create(
                student=stud, preference_number=i, tour_number=new_tour_number)


# Function which is used to normalize char (it removes accent from it):
def normalize_char(c):
    try:
        cname = unicodedata.name(c)
        cname = cname[:cname.index(' WITH')]
        return unicodedata.lookup(cname)
    except (ValueError, KeyError):
        return c


# Function which I use to normalize text (it removes accents)
def normalize_string(s):
    return ''.join(normalize_char(c) for c in s)
