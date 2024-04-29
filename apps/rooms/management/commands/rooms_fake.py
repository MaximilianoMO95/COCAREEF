import random
from django.core.management.base import (BaseCommand, CommandError)
from apps.rooms.models import (Room, RoomType);
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
            help='Delete all rooms',
        )


    def handle(self, *args, **options):
        faker = Faker()

        if options['delete_all']:
            Room.objects.all().delete()
            RoomType.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All rooms deleted'))

        try:
            count = int(options['count'][0])
        except ValueError:
            raise CommandError('"{}" is not a number'.format(options['count'][0]))

        room_types = ['vip', 'tourist']
        for i in range(count):
            room_type = random.choice(room_types)
            room_type_instance, _ = RoomType.objects.get_or_create(name=room_type)
            room_name = 'Habitacion %s' % i

            # Create a fake user
            Room.objects.create(
                name = room_name,
                description = faker.text(),
                capacity = random.randint(1, 5),
                price = random.randint(0, 200000),
                room_type = room_type_instance,
            )

        self.stdout.write(self.style.SUCCESS('Successfully created [%s] fake rooms' % count))

