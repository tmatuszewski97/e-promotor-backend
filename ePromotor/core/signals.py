from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, DeanWorker, Promoter, Student, Record


# Creating Token when new user was created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Deleting associated User when DeanWorker, Promoter or Student was deleted
@receiver(post_delete, sender=DeanWorker)
@receiver(post_delete, sender=Promoter)
@receiver(post_delete, sender=Student)
def delete_user(sender, instance, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()


# Creating Record instances (3 instances for each newly registered Student)
@receiver(post_save, sender=Student)
def create_init_records(sender, instance=None, created=False, **kwargs):
    if created:
        for i in range(1, 4):
            Record.objects.create(
                student=instance, preference_number=i, tour_number=1)
