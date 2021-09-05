from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_pupil = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)


class Pupil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True)


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Training(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    user = models.ManyToManyField(User)


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True)


class Serie(models.Model):
    amount = models.SmallIntegerField()
    kilos = models.SmallIntegerField()
    date = models.DateField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # training = models.ForeignKey(Training, on_delete=models.CASCADE)
