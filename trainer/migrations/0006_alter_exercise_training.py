# Generated by Django 3.2.6 on 2021-09-04 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0005_auto_20210904_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='training',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainer.training'),
        ),
    ]