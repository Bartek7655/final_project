from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from django.shortcuts import redirect, render, resolve_url
from django.views import View
import django.views.generic as gen
from django.urls import reverse_lazy

from trainer.forms import ExerciseFormSet
import trainer.forms as forms
from trainer.models import User, Training, Exercise


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class SignUpView(View):
    def get(self, request):
        return render(request, 'signup_choice.html')


class PupilSignUpView(gen.CreateView):
    model = User
    form_class = forms.PupilForm
    template_name = 'signup_form.html'
    success_url = '/'


class TrainerSignUpView(gen.CreateView):
    model = User
    form_class = forms.TrainerForm
    template_name = 'signup_form.html'
    success_url = '/'


class UserLoginView(gen.CreateView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'home'


class UserEditView(LoginRequiredMixin, gen.UpdateView):
    model = User
    template_name = 'edit_user.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = '/'

    # def get_success_url(self):
    #     # super() # TODO błąd -> .get_success_url()
    #     return resolve_url('home')


class TrainingListView(LoginRequiredMixin, gen.ListView):
    model = Training
    template_name = 'training_list.html'

    def get_queryset(self):
        super().get_queryset()
        user = User.objects.get(pk=self.request.user.pk)
        queryset = Training.objects.filter(user=user)
        return queryset


class TrainingDetailsView(LoginRequiredMixin, gen.DetailView):
    model = Training
    template_name = 'training_details.html'


class TrainingCreateView(LoginRequiredMixin, gen.TemplateView):
    template_name = 'training_create.html'

    def get(self, *args, **kwargs):
        formset_exercise = forms.ExerciseFormSet(queryset=Exercise.objects.none())
        form_training = forms.TrainingForm
        context = {'formset_exercise': formset_exercise,
                   'form_training': form_training}
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        formset_exercise = forms.ExerciseFormSet(self.request.POST)
        form_training = forms.TrainingForm(self.request.POST)

        if formset_exercise.is_valid() and form_training.is_valid():
            user = self.request.user.pk
            training = form_training.save()
            training.user.add(user)
            for form in formset_exercise:
                exercise = form.save()
                exercise.training = training
                exercise.save()

            return redirect(reverse_lazy('home'))

        return self.render_to_response({'formset_exercise': formset_exercise,
                                        'form_training': form_training})
