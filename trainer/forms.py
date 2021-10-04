import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm, modelformset_factory
from django.utils.translation import gettext_lazy as _

from trainer.models import Pupil, Trainer, User, Training, Exercise, Serie, Photo


class PupilForm(UserCreationForm):
    # The form creating a pupil, gives it the flag is_pupil
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
    # The form creating a trainer, gives it the flag is_trainer

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

    # def __init__(self, current_user, *args, **kwargs):
    #     # Overwrites the user field so that only people related to a given trainer are displayed
    #     super(TrainingForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].queryset = self.fields['user'].queryset.filter(pupil__trainer_id=current_user.pk)

    class Meta:
        model = Training
        fields = ['name', 'description', 'pupil', 'trainer']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 2}),
            'pupil': forms.HiddenInput(),
            'trainer': forms.HiddenInput()
        }
        labels = {
            'name': _('Training name'),
            'description': _('Training description'),
            'pupil': _('Pupil')
        }


ExerciseFormSet = modelformset_factory(
    Exercise, fields=('name', 'description', 'amount_serie'),
    extra=1,
    widgets={
        'description': forms.Textarea(attrs={'cols': 30, 'rows': 2})
    },
)

# A separate formset for editing has been added so that there are no additional fields to type
ExerciseEditFormSet = modelformset_factory(
    Exercise, fields=('name', 'description', 'amount_serie'),
    extra=0,
    widgets={
        'description': forms.Textarea(attrs={'cols': 30, 'rows': 2})
    }, )


class SerieDateForm(forms.ModelForm):
    # Extra field to date, entire form created for CreateView
    class Meta:
        model = Serie
        fields = ('date',)

    def clean_date(self):
        # Date validation, future date is invalid
        date = self.cleaned_data['date']
        if datetime.datetime.strptime(str(date), '%Y-%m-%d') > datetime.datetime.now():
            raise ValidationError(_('Invalid date'))
        return date

#get
def serie_formset(how_many):
    ''' Function with formset, so that you can display the number of fields to be entered in accordance with
        the number of series of a given exercise. '''
    SerieFormSet = modelformset_factory(Serie, fields=('amount', 'kilos'), extra=how_many)
    return SerieFormSet


class SearchForm(forms.Form):
    # Search engine form.
    search_by_username = forms.CharField(max_length=100, label='Enter nickname')

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', )
