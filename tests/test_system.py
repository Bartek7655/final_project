import pytest

from trainer.models import User
from system.models import Notifications


@pytest.mark.django_db
def test_notifications_view(client, login_user):
    response = client.get('/notifications/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_send_invitation_view(client, login_user):
    trainer = User.objects.get(username='Trainer')
    pupil = User.objects.get(username='Pupil')

    response = client.get(f'/send-inv/{trainer.pk}/{pupil.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_service_notifications_view(client, login_user, create_notification):
    notification = create_notification
    response = client.get(f'/send-inv/inv-decision/{notification.pk}/delete/')
    assert response.status_code == 302
    assert Notifications.objects.count() == 0
