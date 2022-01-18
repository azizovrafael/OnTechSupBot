# Generated by Django 3.2 on 2022-01-12 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=100, verbose_name='Chat ID: ')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full Name: ')),
                ('username', models.CharField(max_length=100, verbose_name='Username: ')),
            ],
        ),
    ]
