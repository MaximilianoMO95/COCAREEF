import random
from django.core.management.base import (BaseCommand, CommandError)
from apps.rooms.models import (Room, RoomType);
from faker import Faker

class Command(BaseCommand):
    help = 'Manage rooms from command line'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--delete-all',
            action='store_true',
            help='Delete all rooms',
        )
        parser.add_argument(
            '--create-fake-rooms',
            action='store_true',
            help='Creates fake rooms <ex: --create-fake-rooms 20>'
        )
        parser.add_argument('count', nargs=1, type=int, default=1, help='Number of fake rooms to create')


    def handle(self, *args, **options):
        match options:
            case { 'delete_all': True }: self.delete_all()
            case { 'create_fake_rooms': True }: self.create_fake_rooms(options['count'][0])
            case _: self.stdout.write(self.style.WARNING('No action specified. Use --help for more options'))


    def delete_all(self):
        Rooms.objects.all().delete()
        Rooms.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All users deleted'))


    def create_fake_rooms(self, count):
        faker = Faker()

        room_types = ['tourist', 'premium']
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
