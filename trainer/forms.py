import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm, modelformset_factory
from django.utils.translation import gettext_lazy as _

from trainer.models import Pupil, Trainer, User, Training, Exercise, Serie
from trainer import validators


class PupilForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_pupil = True
        user.save()
        permission = Permission.objects.get(codename='pupil')
        user.user_permissions.add(permission)
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
        permission = Permission.objects.get(codename='trainer')
        user.user_permissions.add(permission)
        Trainer.objects.create(user=user)
        return user


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'description', 'user']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 2})
        }
        labels = {
            'name': _('Training name'),
            'description': _('Training description'),
            'user': _('Pupil')
        }


ExerciseFormSet = modelformset_factory(
    Exercise, fields=('name', 'description', 'amount_serie'),
    extra=1,
    widgets={
        'description': forms.Textarea(attrs={'cols': 30, 'rows': 2})
    },
)

ExerciseEditFormSet = modelformset_factory(
    Exercise, fields=('name', 'description', 'amount_serie'),
    extra=0,
    widgets={
        'description': forms.Textarea(attrs={'cols': 30, 'rows': 2})
    }, )


class SerieDateForm(forms.ModelForm):

    class Meta:
        model = Serie
        fields = ('date',)

    def clean_date(self):
        date = self.cleaned_data['date']
        if datetime.datetime.strptime(str(date), '%Y-%m-%d') > datetime.datetime.now():
            raise ValidationError(_('Invalid date'))
        return date


def serie_formset(how_many):
    SerieFormSet = modelformset_factory(
        Serie, fields=('amount', 'kilos'), extra=how_many,
        widgets={

        }
    )
    return SerieFormSet


class SearchForm(forms.Form):
    search_by_username = forms.CharField(max_length=100, label='Enter nickname')