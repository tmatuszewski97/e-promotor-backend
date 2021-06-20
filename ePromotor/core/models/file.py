from django.db import models
from django.conf import settings
from django.utils import timezone


class File (models.Model):
    file = models.FileField(upload_to="files/")
    ROLE_CHOICES = (
        (1, 'administratorzy'),
        (2, 'pracownicy dziekanatu'),
        (3, 'promotorzy'),
        (4, 'studenci'),
        (5, 'tylko ja'),
    )
    shared_for = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=5)
    creation_date = models.DateTimeField(
        verbose_name='creation date', default=timezone.now)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='creator', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'file'
        verbose_name_plural = 'files'

    def __str__(self):
        return '%s %s %s' % (self.file, self.shared_for, self.creator.email)
