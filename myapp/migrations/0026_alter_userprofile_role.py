# Generated by Django 4.2.3 on 2024-03-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_remove_author_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('Learner', 'Learner'), ('Tutor', 'Tutor')], max_length=10),
        ),
    ]
