from django.core.management.base import BaseCommand
from django.db import transaction
from apps.reservations.models import Reservation, ReservationPaymentStatus


class Command(BaseCommand):
    help = 'Deletes reservations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-all',
            action='store_true',
            help='Delete all reservations'
        )
        parser.add_argument(
            '--delete-expired',
            action='store_true',
            help='Delete expired reservations'
        )
        parser.add_argument(
            '--fill-payment-status',
            action='store_true',
            help='Fill payment status table'
        )

    def handle(self, *args, **options):
        match options:
            case { 'delete_all': True }: self.delete_all_reservations()
            case { 'delete_expired': True }: self.delete_expired_reservations()
            case { 'fill_payment_status': True }: self.fill_payment_status()
            case _: self.stdout.write(self.style.WARNING('No action specified. Use --help for more options'))


    def delete_all_reservations(self) -> None:
        Reservation.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All reservations deleted successfully'))


    def delete_expired_reservations(self) -> None:
        Reservation.objects.delete_expired_reservations()
        self.stdout.write(self.style.SUCCESS('Expired reservations deleted successfully'))


    def fill_payment_status(self) -> None:
        if ReservationPaymentStatus.objects.exists():
            self.stdout.write(self.style.WARNING('Payment statuses already exist'))
            return

        with transaction.atomic():
            ReservationPaymentStatus.objects.bulk_create([
                ReservationPaymentStatus(code='NP', name='NOT PAID'),
                ReservationPaymentStatus(code='PP', name='PARTIALLY PAID'),
                ReservationPaymentStatus(code='FP', name='FULLY PAID'),
            ])

        self.stdout.write(self.style.SUCCESS('Payment status created successfully'))
