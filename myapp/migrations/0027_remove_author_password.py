# Generated by Django 4.2.3 on 2024-03-11 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_alter_userprofile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='password',
        ),
    ]