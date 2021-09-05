"""projekt_koncowy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


import trainer.views as trainer

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', trainer.HomeView.as_view(), name='home'),
    path('accounts/signup/', trainer.SignUpView.as_view(), name='signup'),
    path('accounts/signup/pupil/', trainer.PupilSignUpView.as_view(), name='pupil_signup'),
    path('accounts/signup/trainer/', trainer.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('accounts/login/', trainer.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', trainer.UserLogoutView.as_view(), name='logout'),
    path('accounts/edit/<int:pk>/', trainer.UserEditView.as_view(), name='edit'),
    path('training/', trainer.TrainingListView.as_view(), name='training'),
    # path('training/add/', trainer.TrainingCreateView.as_view(), name='training_create'),
    path('training/details/<int:pk>', trainer.TrainingDetailsView.as_view(), name='training_details'),
    path('training/add/exercise/', trainer.ExerciseCreateView.as_view(), name='exercise_create'),

]
