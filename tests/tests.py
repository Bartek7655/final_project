import pytest

from trainer.models import User, Training, Serie, Exercise


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_signup(client):
    response = client.get('/accounts/signup/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_pupil(client, user_permissions):
    response = client.post('/accounts/signup/pupil/',
                           data={'username': 'test123', 'password1': 'ZZddlsa7432', 'password2': 'ZZddlsa7432'})
    assert response.status_code == 302
    user = User.objects.first()
    assert user.username == 'test123'
    assert user.is_trainer == False
    assert user.is_pupil == True


@pytest.mark.django_db
def test_signup_trainer(client, user_permissions):
    response = client.post('/accounts/signup/trainer/',
                           data={'username': 'test123', 'password1': 'ZZddlsa7432', 'password2': 'ZZddlsa7432'})
    assert response.status_code == 302
    user = User.objects.first()
    assert user.username == 'test123'
    assert user.is_pupil == False
    assert user.is_trainer == True


@pytest.mark.django_db
def test_login(client, create_trainer):
    response = client.post('/accounts/login/', {'name': 'Trainer', 'password': 'Testowy123'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(client, login_user):
    response = client.get('/accounts/logout')
    assert response.status_code == 301
    with pytest.raises(TypeError):
        assert response.context['user']


@pytest.mark.django_db
def test_edit_user(client, login_user):
    user = User.objects.get(username='Trainer')
    response = client.post(f'/accounts/edit/{user.pk}/',
                           {'first_name': 'anna', 'last_name': 'samsung', 'email': 'test@gmail.com'})
    assert response.status_code == 302
    user = User.objects.get(username='Trainer')
    assert user.first_name == 'anna'


@pytest.mark.django_db
def test_list_training(client, login_user):
    response = client.get('/training/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_details_training(client, login_user, create_training):
    training = create_training
    response = client.get(f'/training/details/{training.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_training(client, login_user, create_pupil):
    pupil = create_pupil
    response = client.post('/training/add/',
                           {
                               f'name': 'example training name', 'description': 'example training description',
                               'pupil_username': {pupil.username},
                               'form-0-name': 'example exercise name',
                               'form-0-description': 'example exercise description',
                               'form-0-amount_serie': 3,
                               'form-TOTAL_FORMS': 1,
                               'form-INITIAL_FORMS': 0,
                               'form-MIN_NUM_FORMS': 0,
                               'form-MAX_NUM_FORMS': 1000,
                               'form-0-id': ''
                           })
    assert response.status_code == 302
    assert Training.objects.all().count() == 1


@pytest.mark.django_db
def test_edit_training(client, login_user, create_pupil, create_training):
    training = create_training
    pupil = create_pupil
    response = client.post(f'/training/edit/{training.pk}/',
                           {
                               f'name': 'CHANGED', 'description': 'example training description',
                               'pupil_username': {pupil.pk},
                               'form-0-name': 'example exercise name',
                               'form-0-description': 'example exercise description',
                               'form-0-amount_serie': 3,
                               'form-TOTAL_FORMS': 1,
                               'form-INITIAL_FORMS': 0,
                               'form-MIN_NUM_FORMS': 0,
                               'form-MAX_NUM_FORMS': 1000,
                               'form-0-id': ''
                           })
    assert response.status_code == 302
    training = Training.objects.get(pk=training.pk)
    assert training.name == "CHANGED"


@pytest.mark.django_db
def test_create_serie(client, create_exercise, create_pupil):
    client.login(username="Pupil", password="Testowy123")

    exercise = Exercise.objects.first()

    client.post(f'/training/serie/{exercise.pk}/',
                {
                    'date': '2021-09-18',
                    'form-TOTAL_FORMS': '1',
                    'form-INITIAL_FORMS': '0',
                    'form-MIN_NUM_FORMS': '0',
                    'form-MAX_NUM_FORMS': '1000',
                    'form-0-amount': '3',
                    'form-0-kilos': '3',
                    'form-0-id': ''
                })
    assert Serie.objects.all().count() > 0
