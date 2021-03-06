# Generated by Django 3.1.6 on 2021-04-21 17:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=200, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=200, verbose_name='first name')),
                ('last_name', models.CharField(max_length=200, verbose_name='last name')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'administrator'), (2, 'pracownik dziekanatu'), (3, 'promotor'), (4, 'student')], default=4)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Promoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.PositiveSmallIntegerField(choices=[(1, 'prof. dr hab.'), (2, 'dr hab.'), (3, 'dr')], default=3)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('proposed_topics', models.TextField(blank=True, default='', verbose_name='proposed topics')),
                ('unwanted_topics', models.TextField(blank=True, default='', verbose_name='unwanted topics')),
                ('interests', models.TextField(blank=True, default='')),
                ('contact', models.TextField(blank=True, default='')),
                ('max_students_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='max students number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='promoter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'promoters',
                'db_table': 'promoter',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('cycle_degree', models.PositiveSmallIntegerField(choices=[(1, 'pierwszy'), (2, 'drugi')], default=1)),
                ('specialization', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'students',
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_number', models.IntegerField()),
                ('preference_number', models.IntegerField(verbose_name='preference number')),
                ('academic_year', models.CharField(default='2020/2021', max_length=200, verbose_name='academic year')),
                ('was_revoked', models.BooleanField(default=False, verbose_name='was revoked')),
                ('was_sent', models.BooleanField(default=False, verbose_name='was sent')),
                ('was_selected', models.BooleanField(default=None, null=True, verbose_name='was selected')),
                ('promoter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promoter', to='core.promoter')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='core.student')),
            ],
            options={
                'verbose_name_plural': 'records',
                'db_table': 'record',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
                ('shared_for', models.PositiveSmallIntegerField(choices=[(1, 'administratorzy'), (2, 'pracownicy dziekanatu'), (3, 'promotorzy'), (4, 'studenci'), (5, 'tylko ja')], default=5)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'files',
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='DeanWorker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dean_worker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'dean workers',
                'db_table': 'dean_worker',
            },
        ),
    ]
