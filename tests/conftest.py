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
def create_trainer(user_permissions):
    trainer = User.objects.create_user(username='Trainer', password='Testowy123')
    permission = Permission.objects.get(codename='trainer')
    trainer.user_permissions.add(permission)
    return trainer


@pytest.fixture
def create_pupil(user_permissions):
    pupil = User.objects.create_user(username='Pupil', password='Testowy123')
    permission = Permission.objects.get(codename='pupil')
    pupil.user_permissions.add(permission)

    return pupil


@pytest.fixture
def create_training(create_trainer):
    training = Training.objects.create(name='testowy123', description='testowy123')
    training.user.add(User.objects.get(username='Trainer'))
    return training


@pytest.fixture
def login_user(client, create_trainer):
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
