# Generated by Django 5.1.2 on 2024-11-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_bookmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='author_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
