# Generated by Django 4.2.3 on 2024-03-23 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_coursematerial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.coursematerial'),
        ),
    ]