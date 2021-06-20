from rest_framework import permissions
from core.models import Student, Record


# Custom permissions which checks User role


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 1)


class IsDeanWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 2)


class IsPromoter(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 3)


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 4)


class IsAdministratorOrDeanWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == 1 or request.user.role == 2)


class IsNotStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role != 4)


class IsCreatorOfFile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.creator == request.user)


class IsPromoterOfRecord(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.promoter.user == request.user)


# Defined for urls like http://192.168.0.14:8000/api/student/record/13/promoter/
# It checks, is actual logged user can be able to access url with record_id=13
# (he need to be a student in Record instance, where record.id=13)
class IsStudentOfRecordFromUrl(permissions.BasePermission):
    def has_permission(self, request, view):
        id_in_url = view.kwargs.get('pk')

        user = request.user
        student = Student.objects.get(user=user)

        try:
            student_of_record = Record.objects.get(id=id_in_url).student
        except Record.DoesNotExist:
            return False
        else:
            return bool(student == student_of_record)
