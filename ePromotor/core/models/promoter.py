from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Promoter (models.Model):
    TITLE_CHOICES = (
        (1, 'prof. dr hab.'),
        (2, 'dr hab.'),
        (3, 'dr'),
    )
    title = models.PositiveSmallIntegerField(
        choices=TITLE_CHOICES, default=3)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    proposed_topics = models.TextField(
        verbose_name='proposed topics', default="", blank=True)
    unwanted_topics = models.TextField(
        verbose_name='unwanted topics', default="", blank=True)
    interests = models.TextField(default="", blank=True)
    contact = models.TextField(default="", blank=True)
    max_students_number = models.PositiveIntegerField(
        verbose_name='max students number', validators=[MinValueValidator(1)])
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='promoter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'promoter'
        verbose_name_plural = 'promoters'

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.user.email, self.title, self.image, self.proposed_topics, self.unwanted_topics, self.interests, self.contact, self.max_students_number)
