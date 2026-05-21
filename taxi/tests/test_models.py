from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="XYZ12345"
        )

    def test_str_method(self):
        expected_str = (
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_str)

    def test_driver_fields(self):
        self.assertEqual(self.driver.username, "johndoe")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "XYZ12345")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)
