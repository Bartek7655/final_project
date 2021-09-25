from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_pupil = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)


class Pupil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='pupil')
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, related_name='pupil')


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='trainer')


class Training(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    user = models.ManyToManyField(User)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    amount_serie = models.SmallIntegerField()
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, related_name='exercise')


class Serie(models.Model):
    amount = models.SmallIntegerField()
    kilos = models.SmallIntegerField()
    serie_number = models.SmallIntegerField()
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='serie')



