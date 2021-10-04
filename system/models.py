from django.db import models

import trainer.models


class Notification(models.Model):
    notification = models.TextField()
    to_user = models.ForeignKey(trainer.models.User, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(trainer.models.User, on_delete=models.CASCADE, null=True, related_name='invitation')
    is_invitation = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)


class Message(models.Model):
    to_user = models.ForeignKey(trainer.models.User, on_delete=models.CASCADE, related_name='received_messages')
    from_user = models.ForeignKey(trainer.models.User, on_delete=models.CASCADE, related_name='sent_messages')
    date = models.DateTimeField(auto_now=True)
    message = models.TextField()

