# Generated by Django 3.2.4 on 2021-07-23 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarian',
            name='title',
            field=models.CharField(default='Mr', max_length=4),
        ),
    ]
