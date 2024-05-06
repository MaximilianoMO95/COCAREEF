# Generated by Django 5.0.4 on 2024-05-06 00:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationPaymentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='start_date')),
                ('days_of_stay', models.PositiveIntegerField(default=1, verbose_name='days_of_stay')),
                ('deposit_percentage', models.PositiveSmallIntegerField(default=30, verbose_name='deposit_percentage')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.room', verbose_name='room')),
            ],
            options={
                'permissions': [('can_view_reservation', '[Custom] Can view a reservation'), ('can_add_reservation', '[Custom] Can add a reservation'), ('can_change_reservation', '[Custom] Can change a reservation'), ('can_delete_reservation', '[Custom] Can delete a reservation')],
            },
        ),
    ]