from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver


DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverListViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_admin", password="password123"
        )
        self.client.login(username="test_admin", password="password123")

        self.driver1 = Driver.objects.create_user(
            username="alex_driver", license_number="LIC001"
        )
        self.driver2 = Driver.objects.create_user(
            username="john_driver", license_number="LIC002"
        )
        self.driver3 = Driver.objects.create_user(
            username="bob_racer", license_number="LIC003"
        )

    def test_retrieve_drivers_without_search(self):
        res = self.client.get(DRIVERS_URL)

        self.assertEqual(res.status_code, 200)
        drivers = res.context["object_list"]

        self.assertEqual(len(drivers), 4)

    def test_search_driver_by_username_case_insensitive(self):
        res = self.client.get(DRIVERS_URL, data={"title": "DRIV"})

        self.assertEqual(res.status_code, 200)
        drivers = res.context["object_list"]

        self.assertEqual(len(drivers), 2)
        self.assertTrue(any(d.username == "alex_driver" for d in drivers))
        self.assertTrue(any(d.username == "john_driver" for d in drivers))
        self.assertFalse(any(d.username == "bob_racer" for d in drivers))

    def test_search_no_results(self):
        res = self.client.get(DRIVERS_URL, data={"title": "non_existent_name"})

        self.assertEqual(res.status_code, 200)
        drivers = res.context["object_list"]

        self.assertEqual(len(drivers), 0)

    def test_search_form_initial_value(self):
        search_term = "alex"
        res = self.client.get(DRIVERS_URL, data={"title": search_term})

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(
            res.context["search_form"].initial["title"], search_term
        )
