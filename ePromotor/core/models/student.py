from django.db import models
from django.conf import settings


class Student (models.Model):
    index = models.IntegerField()
    CYCLE_DEGREE_CHOICES = (
        (1, 'pierwszy'),
        (2, 'drugi'),
    )
    cycle_degree = models.PositiveSmallIntegerField(
        choices=CYCLE_DEGREE_CHOICES, default=1)
    specialization = models.CharField(max_length=200)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='student', on_delete=models.CASCADE)

    class Meta:
        db_table = 'student'
        verbose_name_plural = 'students'

    def __str__(self):
        return '%s %s %s' % (self.user.email, self.index, self.specialization)
