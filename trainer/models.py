from django.db import models
from django.contrib.auth.models import AbstractUser
import stdimage

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
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='training')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='training')


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


class Weight(models.Model):
    kilos = models.SmallIntegerField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Photo(models.Model):
    image = stdimage.StdImageField(upload_to='images/',
                                   variations={
                                       'large': (600, 400),
                                       'thumbnail': (100, 100, True),
                                       'medium': (300, 200),
                                   })
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo')



