from django.db import models
from django.conf import settings


class DeanWorker (models.Model):
    contact = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='dean_worker', on_delete=models.CASCADE)

    class Meta:
        db_table = 'dean_worker'
        verbose_name_plural = 'dean workers'

    def __str__(self):
        return '%s %s' % (self.user.email, self.contact)
