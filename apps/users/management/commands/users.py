import random
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from faker import Faker

from apps.users.models import (Customer, Employee, User)

class Command(BaseCommand):
    help = 'Manage users from command line'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--delete-all',
            action='store_true',
            help='Delete all users',
        )
        parser.add_argument(
            '--create-fake-users',
            action='store_true',
            help='Creates fake users <ex: --create-fake-users 20>'
        )
        parser.add_argument(
            '--set-group-permissions',
            action='store_true',
            help='Set group permissions',
        )
        parser.add_argument(
            'count',
            default='0',
            nargs='?',
            type=str,
            help='Number of fake users to create',
        )


    def handle(self, *args, **options):
        match options:
            case { 'set_group_permissions': True }: self.set_group_permissions()
            case { 'delete_all': True }: self.delete_all()
            case { 'create_fake_users': True }: self.create_fake_users(options['count'][0])
            case _: self.stdout.write(self.style.WARNING('No action specified. Use --help for more options'))


    def delete_all(self):
        Customer.objects.all().delete()
        Employee.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All users deleted'))


    def create_fake_users(self, count: str):
        faker = Faker()

        user_type = random.choice([0, 1])
        for _ in range(int(count)):
            user_instance = User.objects.create(
                username='Faker-' + faker.user_name(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
            )

            if user_type == 0:
                Customer.objects.create(user=user_instance, dni=random.randint(12345678, 123456789))
            else:
                Employee.objects.create(user=user_instance, rut=random.randint(12345678, 123456789))

        self.stdout.write(self.style.SUCCESS('Successfully created [%s] fake users' % count))


    def set_group_permissions(self):
        #customer_group, _ = Group.objects.get_or_create(name='customer')
        employee_group, _ = Group.objects.get_or_create(name='employee')

        user_permissions = Permission.objects.filter(
            content_type__app_label='users',
            codename__in=['can_view_admin_panel']
        )

        reservation_permissions = Permission.objects.filter(
            content_type__app_label='reservations',
            codename__in=[
                'can_view_reservation',
                'can_add_reservation',
                'can_delete_reservation',
                'can_change_reservation'
            ]
        )
        for permission in reservation_permissions:
            employee_group.permissions.add(permission)

        for permission in user_permissions:
            employee_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Permissions set for employee group'))
