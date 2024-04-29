# Generated by Django 5.0.4 on 2024-04-29 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=15, verbose_name='Employee ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]