# Generated by Django 5.0.4 on 2024-04-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='employee_id',
        ),
        migrations.AddField(
            model_name='employee',
            name='rut',
            field=models.CharField(default=0, max_length=15, verbose_name='RUT'),
            preserve_default=False,
        ),
    ]
