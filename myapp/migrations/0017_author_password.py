# Generated by Django 4.2.3 on 2024-03-09 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_author_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
