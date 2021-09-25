import pytest
from django.test import Client
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from trainer.models import User, Pupil, Trainer, Training, Exercise


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user_permissions():
    ct = ContentType.objects.get_for_model(Pupil)

    Permission.objects.create(codename='pupil',
                              name='All the main permissions for the pupil.',
                              content_type=ct)

    ct = ContentType.objects.get_for_model(Trainer)

    Permission.objects.create(codename='trainer',
                              name='All the main permissions for the trainer.',
                              content_type=ct)


@pytest.fixture
def create_users(user_permissions):
    trainer = User.objects.create_user(username='Trainer', password='Testowy123',
                                       is_trainer=True)
    Trainer.objects.create(user=trainer)
    permission = Permission.objects.get(codename='trainer')
    trainer.user_permissions.add(permission)

    pupil = User.objects.create_user(username='Pupil', password='Testowy123',
                                     is_pupil=True)

    Pupil.objects.create(user=pupil, trainer=Trainer.objects.first())
    permission = Permission.objects.get(codename='pupil')
    pupil.user_permissions.add(permission)

    return trainer, pupil


@pytest.fixture
def create_training(create_users):
    training = Training.objects.create(name='testowy123', description='testowy123')
    training.user.add(User.objects.get(username='Trainer'))
    return training


@pytest.fixture
def login_user(client, create_users):
    return client.login(username='Trainer', password='Testowy123')


@pytest.fixture
def create_exercise(create_training):
    exercise = Exercise.objects.create(
        name='name_exercise',
        description='description_exercise',
        amount_serie=1,
        training=create_training
    )
    return exercise

