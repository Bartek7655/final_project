from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from trainer.models import Pupil, Trainer

ct = ContentType.objects.get_for_model(Pupil)

Permission.objects.create(codename='pupil',
                          name='All the main permissions for the pupil.',
                          content_type=ct)

ct = ContentType.objects.get_for_model(Trainer)

Permission.objects.create(codename='trainer',
                          name='All the main permissions for the trainer.',
                          content_type=ct)
