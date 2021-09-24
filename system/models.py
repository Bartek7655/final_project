from django.db import models

import trainer.models


class Notifications(models.Model):
    notification = models.TextField()
    to_user = models.ForeignKey(trainer.models.User, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(trainer.models.User, on_delete=models.CASCADE, null=True, related_name='invitation')
    is_invitation = models.BooleanField(default=False)
