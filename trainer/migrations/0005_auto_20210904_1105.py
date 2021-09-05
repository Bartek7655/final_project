# Generated by Django 3.2.6 on 2021-09-04 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0004_training_exercise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='exercise',
        ),
        migrations.AddField(
            model_name='exercise',
            name='training',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trainer.training'),
            preserve_default=False,
        ),
    ]
