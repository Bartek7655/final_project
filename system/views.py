from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import django.views.generic as gen

from system.models import Notifications
from trainer.models import User


class NotificationsView(LoginRequiredMixin, gen.ListView):
    model = Notifications
    template_name = 'system/notifications.html'

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        if user.is_pupil and user.pupil.trainer == None:
            queryset = Notifications.objects.filter(to_user=user)
        elif user.is_pupil and user.pupil.trainer != None:
            queryset = Notifications.objects.filter(to_user=user, is_invitation=False)
        else:
            queryset = Notifications.objects.filter(to_user=user)

        return queryset


class SendInvitationView(LoginRequiredMixin, gen.View):

    def get(self, request, *args, **kwargs):
        trainer = User.objects.get(pk=self.kwargs['from_pk'])
        pupil = User.objects.get(pk=self.kwargs['to_pk'])
        notification = f"You have an invitation from the trainer {trainer.username}"
        if not Notifications.objects.filter(to_user=pupil, from_user=trainer).exists():
            Notifications.objects.create(
                notification=notification,
                from_user=trainer,
                to_user=pupil,
                is_invitation=True
            )
        else:
            request.session['error'] = 'You have already sent the invitation'
        return redirect('search_pupils')


class NotificationsServiceView(LoginRequiredMixin, gen.View):
    def get(self, request, *args, **kwargs):
        notification = Notifications.objects.get(pk=kwargs['notif_pk'])
        pupil = User.objects.get(pk=notification.to_user.pk)
        try:
            trainer = User.objects.get(pk=notification.from_user.pk)
        except AttributeError:
            None
        if kwargs['decision'] == 'yes':
            pupil.pupil.trainer = trainer.trainer
            pupil.pupil.save()
            notification.delete()
            notification = f"{pupil.username} accepted the invitation."

        elif kwargs['decision'] == 'no':
            notification.delete()
            notification = f"{pupil.username} did not accept the invitation."

        elif kwargs['decision'] == 'delete':
            notification.delete()
            return redirect('notifications')

        Notifications.objects.create(
            notification=notification,
            to_user=trainer,
            is_invitation=False
        )
        return redirect('notifications')
