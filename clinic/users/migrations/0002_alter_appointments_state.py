# Generated by Django 4.0.2 on 2022-02-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='state',
            field=models.CharField(choices=[('canceld by doctor', 'canceld by doctor'), ('canceld', 'canceld'), ('in processing', 'in processing'), ('missed', 'missed'), ('finished', 'finished'), ('reschedule', 'reschedule')], max_length=20, null=True),
        ),
    ]
