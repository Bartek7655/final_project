from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db import models
from django.forms import ModelForm, modelformset_factory

from trainer.models import Pupil, Trainer, User, Training, Exercise


class PupilForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_pupil = True
        user.save()
        Pupil.objects.create(user=user)
        return user


class TrainerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_trainer = True
        user.save()
        Trainer.objects.create(user=user)
        return user


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'description']


ExerciseFormSet = modelformset_factory(
    Exercise, fields=('name', 'description'), extra=1)
