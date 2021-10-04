from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.views import View
import django.views.generic as gen
from django.urls import reverse_lazy

import trainer.forms as forms
from trainer.models import User, Training, Exercise, Serie, Photo, Pupil, Weight
from system.models import Notification


class HomeView(View):
    # this view displays the home page
    def get(self, request):
        return render(request, 'trainer/home.html')


class SignUpView(View):
    # View for selecting a profile for registration
    def get(self, request):
        return render(request, 'trainer/signup_choice.html')


class PupilSignUpView(gen.CreateView):
    # View for pupil registration
    model = User
    form_class = forms.PupilForm
    template_name = 'trainer/signup_form.html'
    success_url = '/'


class TrainerSignUpView(gen.CreateView):
    # View for trainer registration
    model = User
    form_class = forms.TrainerForm
    template_name = 'trainer/signup_form.html'
    success_url = '/'


class UserLoginView(LoginView):
    # Login view
    template_name = 'trainer/login.html'


class UserLogoutView(LogoutView):
    # Logout view
    template_name = 'trainer/logout.html'
    next_page = 'home'


class UserEditView(LoginRequiredMixin, gen.UpdateView):
    # View for editing user data
    model = User
    template_name = 'trainer/edit_user.html'
    fields = ('first_name', 'last_name', 'email',)
    success_url = '/'


class TrainingListView(LoginRequiredMixin, gen.ListView):
    # The view showing all trainings also shows the most recent (by date) training
    model = Training
    template_name = 'trainer/training_list.html'

    def get_queryset(self):
        # I only download trainings related to a given user
        queryset = Training.objects.filter(pupil_id=self.kwargs['pupil_pk'])
        return queryset

    def get_context_data(self, **kwargs):
        # Adds context with the last training session
        context = super().get_context_data()
        pupil = Pupil.objects.get(pk=self.kwargs['pupil_pk'])
        trainings = Training.objects.filter(pupil_id=pupil.pk)
        latest_entry_serie = None
        context['pupil'] = pupil
        for training in trainings:
            exercises = Exercise.objects.filter(training_id=training.id)
            for exercise in exercises:
                series = Serie.objects.filter(exercise_id=exercise.id)
                for serie in series:
                    if serie == None:
                        continue
                    elif latest_entry_serie == None:
                        latest_entry_serie = serie
                    elif serie.date > latest_entry_serie.date:
                        latest_entry_serie = serie

        try:
            training = latest_entry_serie.exercise.training
            exercises = Exercise.objects.filter(training_id=training.id)
            series = []
            for exercise in exercises:
                helper = Serie.objects.filter(exercise_id=exercise.id)
                for serie in helper:
                    if serie.date == latest_entry_serie.date:
                        series.append(serie)
            context['training'] = training
            context['exercises'] = exercises
            context['series'] = series

        except:
            return context

        return context


class TrainingDetailsView(LoginRequiredMixin, gen.DetailView):
    # View for training details
    model = Training
    template_name = 'trainer/training_details.html'

    def get_queryset(self):
        queryset = Training.objects.filter(trainer_id=self.request.user.pk)
        return queryset


class TrainingDeleteView(PermissionRequiredMixin, gen.DeleteView):
    # View for training delete
    permission_required = 'trainer.trainer'
    model = Training
    template_name = 'trainer/training_delete.html'
    success_url = '/training/'

    def get_queryset(self):
        queryset = Training.objects.filter(trainer_id=self.request.user.pk)
        return queryset


class TrainingEditView(PermissionRequiredMixin, gen.UpdateView):
    # View for training edit
    permission_required = 'trainer.trainer'
    model = Training
    template_name = 'trainer/training_edit.html'
    fields = ('name', 'description')
    success_url = '/training/'

    def get_queryset(self):
        queryset = Training.objects.filter(trainer_id=self.request.user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        # This method filters exercises that are specific to the training session only
        context = super(TrainingEditView, self).get_context_data(**kwargs)
        training_pk = self.kwargs['pk']
        exercises = Exercise.objects.filter(training_id=training_pk)
        exercises_formset = forms.ExerciseEditFormSet(queryset=exercises)
        context['exercises_formset'] = exercises_formset
        return context

    def post(self, request, *args, **kwargs):
        # This method records training related exercises
        super().post(self, request, *args, **kwargs)
        formset_exercise = forms.ExerciseEditFormSet(self.request.POST)

        if formset_exercise.is_valid():
            for form in formset_exercise:
                form.save()
        else:
            print('error')
        training = Training.objects.get(pk=kwargs['pk'])
        return redirect('training', pupil_pk=training.pupil.pk)


class TrainingCreateView(PermissionRequiredMixin, gen.CreateView):
    # The view that creates the training
    model = Training
    permission_required = 'trainer.trainer'
    template_name = 'trainer/training_create.html'

    def get(self, *args, **kwargs):
        # A formset with exercises is added to the context
        pupil = Pupil.objects.get(pk=self.kwargs['pupil_pk'])

        if pupil.trainer == self.request.user.trainer:
            formset_exercise = forms.ExerciseFormSet(queryset=Exercise.objects.none())
            form_training = forms.TrainingForm(initial={'pupil': pupil, 'trainer': self.request.user.trainer})
            context = {'formset_exercise': formset_exercise,
                       'form_training': form_training}
            return self.render_to_response(context)
        else:
            # TODO Error404 <--
            return self.render_to_response({})

    def post(self, *args, **kwargs):
        # Saving formset and create notification for pupil
        formset_exercise = forms.ExerciseFormSet(self.request.POST)
        form_training = forms.TrainingForm(data=self.request.POST)
        pupil = Pupil.objects.get(pk=self.request.POST['pupil'])
        if formset_exercise.is_valid() and form_training.is_valid():
            training = form_training.save()
            for form in formset_exercise:
                exercise = form.save()
                exercise.training = training
                exercise.save()

            # TODO function notifications
            Notification.objects.create(
                to_user=pupil.user,
                notification=f'{self.request.user.username} has created a training, you will find it in your training list.',
                is_invitation=False
            )

            return redirect('training', pupil_pk=pupil.pk)

        return self.render_to_response({'formset_exercise': formset_exercise,
                                        'form_training': form_training})


class SerieCreateView(PermissionRequiredMixin, gen.CreateView):
    # A view that saves series taken by the user
    permission_required = 'trainer.pupil'
    model = Serie
    form_class = forms.SerieDateForm
    template_name = 'trainer/serie_create.html'

    def get_context_data(self, **kwargs):
        # Method adds to the formset context with the number of series for a given exercise
        context = super(SerieCreateView, self).get_context_data(**kwargs)
        exercise_pk = self.kwargs['pk']
        exercise = Exercise.objects.get(pk=exercise_pk)
        formset = forms.serie_formset(exercise.amount_serie)
        context['formset'] = formset(queryset=Serie.objects.none())
        context['exercise'] = Exercise.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        # Method saves formsets.
        exercise_pk = self.kwargs['pk']
        exercise = Exercise.objects.get(pk=exercise_pk)
        date = forms.SerieDateForm(self.request.POST)
        formset_serie = forms.serie_formset(exercise.amount_serie)
        formset_serie = formset_serie(self.request.POST)
        if formset_serie.is_valid() and date.is_valid():
            date = self.request.POST['date']
            number = 1
            for form in formset_serie:
                serie = form.save(commit=False)
                serie.exercise = exercise
                serie.date = date
                serie.serie_number = number
                serie.save()
                number += 1
            return redirect(f'/training/details/{exercise.training_id}')
        return self.render_to_response(context={'formset': formset_serie,
                                                'exercise': Exercise.objects.get(pk=self.kwargs['pk']),
                                                'form': forms.SerieDateForm(self.request.POST)})


class SeriePreviewView(PermissionRequiredMixin, gen.TemplateView):
    # View for the training overview.
    permission_required = 'trainer.trainer'
    template_name = 'trainer/serie_preview.html'

    def get_context_data(self, **kwargs):
        # The method creates a list to handle regroup on the template side
        context = super().get_context_data(**kwargs)
        training = Training.objects.get(pk=self.kwargs['pk'])
        series = Serie.objects.filter(exercise__training=training)
        series_list = []

        for serie in series:
            series_list.append({'amount': serie.amount,
                                'kilos': serie.kilos,
                                'serie_number': serie.serie_number,
                                'date': serie.date,
                                'exercise': serie.exercise})

        context['series_list'] = series_list
        return context


class SearchPupilsView(LoginRequiredMixin, gen.FormView):
    # The view it is looking for pupil
    template_name = 'trainer/search_user.html'
    form_class = forms.SearchForm
    success_url = '/search/user/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'error' in self.request.session:
            context['error'] = self.request.session['error']
            del self.request.session['error']
        return context

    def post(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        nickname = self.request.POST.get('search_by_username')
        pupils = Pupil.objects.filter(user__username__icontains=nickname)
        context['pupils'] = pupils
        return self.render_to_response(context)


class ActivePupilsView(PermissionRequiredMixin, gen.ListView):
    # View listing students
    model = Pupil
    template_name = 'trainer/active_pupils.html'
    permission_required = 'trainer.trainer'

    def get_queryset(self):
        # Method that finds only related pupils
        queryset = Pupil.objects.filter(trainer_id=self.request.user.pk)
        return queryset


class PupilOverView(PermissionRequiredMixin, gen.DetailView):
    # View for viewing the pupil's profile
    model = User
    template_name = 'trainer/pupil_overview.html'
    permission_required = 'trainer.trainer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_user'] = self.request.user.pk
        return context


class DeleteFromPupilsView(PermissionRequiredMixin, gen.View):
    # Removes pupil from the pupil's list and create notification for pupil
    permission_required = 'trainer.trainer'

    def get(self, request, *args, **kwargs):
        pupil = Pupil.objects.get(pk=kwargs['pupil_pk'])
        pupil.trainer = None
        pupil.save()
        Notification.objects.create(
            to_user_id=kwargs['pupil_pk'],
            notification=f'{self.request.user.username} removed you from the list of pupils.',
            is_invitation=False
        )
        return redirect('active_pupils')


class WeightListView(LoginRequiredMixin, gen.ListView):
    model = Weight
    template_name = 'trainer/weight_list.html'

    def get_queryset(self):
        queryset = Weight.objects.filter(user=self.kwargs['pupil_pk'])
        return queryset


class AddPhotoView(LoginRequiredMixin, gen.CreateView):
    template_name = 'trainer/add_photo.html'
    model = Photo
    form_class = forms.PhotoForm
    success_url = '/photos/'

    def post(self, request, *args, **kwargs):
        form = forms.PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = self.request.user
            photo.save()
            return redirect('/photos/')
        return super().render_to_response({'form': form})


class PhotosListView(LoginRequiredMixin, gen.ListView):
    model = Photo
    template_name = 'trainer/photos_list.html'

    def get_queryset(self):
        queryset = Photo.objects.filter(user=self.kwargs['pupil_pk'])
        return queryset


class AdditionalInformationView(LoginRequiredMixin, gen.DetailView):
    model = User
    template_name = 'trainer/additional_information.html'
