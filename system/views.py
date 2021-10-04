from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import django.views.generic as gen
from django.urls import reverse

import system.forms as forms
from system.models import Notification, Message
from trainer.models import User


class NotificationsView(LoginRequiredMixin, gen.ListView):
    model = Notification
    template_name = 'system/notifications.html'

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.pk)
        if user.is_pupil and user.pupil.trainer == None:
            queryset = Notification.objects.filter(to_user=user).order_by('-date')
        elif user.is_pupil and user.pupil.trainer != None:
            queryset = Notification.objects.filter(to_user=user, is_invitation=False)
        else:
            queryset = Notification.objects.filter(to_user=user)

        return queryset


class SendInvitationView(LoginRequiredMixin, gen.View):

    def get(self, request, *args, **kwargs):
        trainer = User.objects.get(pk=self.kwargs['from_pk'])
        pupil = User.objects.get(pk=self.kwargs['to_pk'])
        notification = f"You have an invitation from the trainer {trainer.username}"
        if not Notification.objects.filter(to_user=pupil, from_user=trainer).exists():
            Notification.objects.create(
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
        notification = Notification.objects.get(pk=kwargs['notif_pk'])
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

        Notification.objects.create(
            notification=notification,
            to_user=trainer,
            is_invitation=False
        )
        return redirect('notifications')


class MessagesView(gen.CreateView):
    model = Message
    form_class = forms.MessageForm
    template_name = 'system/messages.html'

    def get_context_data(self, **kwargs):
        # TODO Można jakoś według daty dla pewności to uporządkować?
        context = super().get_context_data(**kwargs)
        from_user = User.objects.get(pk=self.kwargs['from_pk'])
        messages_one = Message.objects.filter(to_user_id=self.request.user, from_user_id=from_user)
        messages_two = Message.objects.filter(to_user_id=from_user, from_user_id=self.request.user)
        messages = [*messages_one, *messages_two]
        context['messages'] = messages
        form = forms.MessageForm(initial={
            'to_user': self.kwargs['from_pk'],
            'from_user': self.request.user
        })
        context['form'] = form
        return context

    def get_success_url(self):
        return reverse('messages', kwargs={'from_pk': self.kwargs['from_pk']})
