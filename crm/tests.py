from django.test import TestCase

from .forms import ReservationForm
from .models import Client, Reservation


class ReservationFormTests(TestCase):
    def test_saves_reservation_with_new_client(self):
        form = ReservationForm(
            data={
                'client_name': 'Иван',
                'date': '01.01.2026',
                'start_time': '10:00',
                'end_time': '11:00',
                'table_number': 1,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        reservation = form.save()
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(reservation.client.name, 'Иван')
        self.assertEqual(Reservation.objects.count(), 1)

    def test_reuses_existing_client_by_name(self):
        existing = Client.objects.create(name='Мария', phone='123')
        form = ReservationForm(
            data={
                'client_name': 'Мария',
                'date': '01.01.2026',
                'start_time': '10:00',
                'end_time': '11:00',
                'table_number': 2,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        reservation = form.save()
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(reservation.client_id, existing.id)

    def test_validates_time_order(self):
        form = ReservationForm(
            data={
                'client_name': 'Иван',
                'date': '01.01.2026',
                'start_time': '11:00',
                'end_time': '10:00',
                'table_number': 1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('end_time', form.errors)
