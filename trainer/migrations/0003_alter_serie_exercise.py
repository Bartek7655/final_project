# Generated by Django 3.2.7 on 2021-09-15 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0002_alter_serie_exercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serie',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.exercise'),
        ),
    ]
