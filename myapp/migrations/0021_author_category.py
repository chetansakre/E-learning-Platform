# Generated by Django 4.2.3 on 2024-03-11 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_remove_author_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.categories'),
        ),
    ]
