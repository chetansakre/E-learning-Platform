# Generated by Django 4.2.3 on 2024-03-23 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_video_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.coursematerial'),
        ),
    ]
