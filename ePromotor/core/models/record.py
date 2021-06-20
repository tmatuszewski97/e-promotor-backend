from django.db import models
from .promoter import Promoter
from .student import Student
from django.utils import timezone


class Record (models.Model):
    tour_number = models.IntegerField()
    preference_number = models.IntegerField(verbose_name='preference number')
    academic_year = models.CharField(
        verbose_name='academic year', default=(str(timezone.now().year-1) + "/" + str(timezone.now().year)), max_length=200)
    was_revoked = models.BooleanField(
        verbose_name='was revoked', default=False)
    was_sent = models.BooleanField(verbose_name='was sent', default=False)
    was_selected = models.BooleanField(
        verbose_name='was selected', null=True, default=None)
    promoter = models.ForeignKey(
        Promoter, related_name='promoter', null=True, blank=True, on_delete=models.SET_NULL)
    student = models.ForeignKey(
        Student, related_name='student', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'record'
        verbose_name_plural = 'records'

    def __str__(self):
        if (self.promoter != None):
            promoter_email = self.promoter.user.email
        else:
            promoter_email = None
        return '%s %s %s %s %s %s %s %s' % (self.tour_number, self.preference_number, self.academic_year, self.was_revoked, self.was_sent, self.was_selected, promoter_email, self.student.user.email)
