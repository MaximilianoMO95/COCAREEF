import random
from django.core.management.base import (BaseCommand, CommandError)
from apps.users.models import (Customer, User)
from faker import Faker

class Command(BaseCommand):
    help = 'Creates a set of fake data'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('count', nargs=1, type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete-all',
            action='store_true',
            help='Delete all users',
        )


    def handle(self, *args, **options):
        faker = Faker()

        if options['delete_all']:
            Customer.objects.all().delete()
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All users deleted'))

        try:
            count = int(options['count'][0])
        except ValueError:
            raise CommandError('"{}" is not a number'.format(options['count'][0]))

        for _ in range(count):
            user_instance = User.objects.create(
                username = faker.user_name(),
                first_name = faker.first_name(),
                last_name = faker.last_name(),
                email = faker.email(),
            )

            Customer.objects.create(user = user_instance, dni = random.randint(12345678, 123456789))

        self.stdout.write(self.style.SUCCESS('Successfully created [%s] fake users' % count))
