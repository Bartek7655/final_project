from django.shortcuts import render, redirect
import django.views.generic as gen

from system.models import Notifications
from trainer.models import User


class NotificationsView(gen.ListView):
    model = Notifications
    template_name = 'system/notifications.html'

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        if user.is_pupil and user.pupil.trainer == None:
            queryset = Notifications.objects.filter(to_user=user, is_invitation=True)
        elif user.is_pupil and user.pupil.trainer != None:
            queryset = Notifications.objects.filter(to_user=user, is_invitation=False)
        else:
            queryset = Notifications.objects.filter(to_user=user)

        return queryset


class SendInvitationView(gen.View):

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


class InvitationServiceView(gen.View):
    def get(self, request, *args, **kwargs):
        notification = Notifications.objects.get(pk=kwargs['notif_pk'])
        pupil = User.objects.get(pk=notification.to_user.pk)
        trainer = User.objects.get(pk=notification.from_user.pk)
        if kwargs['decision'] == 'yes':
            pupil.pupil.trainer = trainer.trainer
            pupil.pupil.save()
            notification.delete()
        elif kwargs['decision'] == 'no':
            notification.delete()
        return redirect('notifications')
