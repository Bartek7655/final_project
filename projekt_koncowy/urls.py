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

from django.conf import settings
from django.conf.urls.static import static

import trainer.views as trainer
import system.views as system

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', trainer.HomeView.as_view(), name='home'),
                  path('accounts/signup/', trainer.SignUpView.as_view(), name='signup'),
                  path('accounts/signup/pupil/', trainer.PupilSignUpView.as_view(), name='pupil_signup'),
                  path('accounts/signup/trainer/', trainer.TrainerSignUpView.as_view(), name='trainer_signup'),
                  path('accounts/login/', trainer.UserLoginView.as_view(), name='login'),
                  path('accounts/logout/', trainer.UserLogoutView.as_view(), name='logout'),
                  path('accounts/edit/<int:pk>/', trainer.UserEditView.as_view(), name='edit'),
                  path('training/<int:pupil_pk>/', trainer.TrainingListView.as_view(), name='training'),
                  path('training/details/<int:pk>/', trainer.TrainingDetailsView.as_view(), name='training_details'),
                  path('training/add/<int:pupil_pk>/', trainer.TrainingCreateView.as_view(), name='training_create'),
                  path('training/edit/<int:pk>/', trainer.TrainingEditView.as_view(), name='training_edit'),
                  path('training/delete/<int:pk>/', trainer.TrainingDeleteView.as_view(), name='training_delete'),
                  path('training/series/<int:pk>/', trainer.SerieCreateView.as_view(), name='serie_create'),
                  path('training/seriespreview/<int:pk>/', trainer.SeriePreviewView.as_view(), name='serie_preview'),
                  path('search/user/', trainer.SearchPupilsView.as_view(), name='search_pupils'),
                  path('pupils/', trainer.ActivePupilsView.as_view(), name='active_pupils'),
                  path('pupils/<int:pk>/', trainer.PupilOverView.as_view(), name='pupil_overview'),
                  path('notifications/', system.NotificationsView.as_view(), name='notifications'),
                  path('send-inv/<int:from_pk>/<int:to_pk>/', system.SendInvitationView.as_view(),
                       name='send_invitation'),
                  path('send-inv/inv-decision/<int:notif_pk>/<str:decision>/',
                       system.NotificationsServiceView.as_view(),
                       name='invitation_service'),
                  path('pupils/delete-from-pupils/<int:pupil_pk>', trainer.DeleteFromPupilsView.as_view(),
                       name='delete_pupil'),
                  path('weight/<int:pupil_pk>', trainer.WeightListView.as_view(), name='weight_list'),
                  path('messages/<int:from_pk>', system.MessagesView.as_view(), name='messages'),
                  path('photos/add/', trainer.AddPhotoView.as_view(), name='add_photo'),
                  path('photos/<int:pupil_pk>/', trainer.PhotosListView.as_view(), name='photos_list'),
                  path('user/information/<int:pk>/', trainer.AdditionalInformationView.as_view(),
                       name='additional_information'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
