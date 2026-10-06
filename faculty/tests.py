from datetime import date, timedelta
from unittest.mock import patch

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.forms import modelform_factory
from django.test import TransactionTestCase

from .models import Department, ExchangeProgram, HomePage, Program, Teacher


class FacultyTest(TransactionTestCase):
    def migrate_to(self, name):
        executor = MigrationExecutor(connection)
        target = [("faculty", name)]
        executor.migrate(target)
        if name:
            return executor.loader.project_state(target).apps

    def test_site_and_migration_round_trip(self):
        latest = "0006_exchange_places"
        self.addCleanup(self.migrate_to, latest)
        original = list(ExchangeProgram.objects.order_by("pk").values())
        admin_user = get_user_model().objects.create_superuser(
            username="test-admin", password="test-only-password",
        )

        for model in (HomePage, Department, Program, Teacher, ExchangeProgram):
            self.assertTrue(admin.site.is_registered(model))
        self.client.force_login(admin_user)
        for model in (HomePage, Department, Program, Teacher, ExchangeProgram):
            self.assertEqual(self.client.get(f"/admin/faculty/{model._meta.model_name}/").status_code, 200)
        self.client.logout()

        def check_pages():
            for path in ("/", "/programs/", "/departments/", "/exchange/", "/admin/login/"):
                self.assertEqual(self.client.get(path).status_code, 200, path)
            for department in Department.objects.all():
                response = self.client.get(f"/departments/{department.pk}/")
                self.assertContains(response, department.name)
                self.assertContains(response, department.head)
                for teacher in department.teachers.all():
                    for value in (teacher.name, teacher.position, teacher.degree):
                        self.assertContains(response, value)
            listing = self.client.get("/programs/")
            for program in Program.objects.all():
                self.assertContains(listing, " ".join(program.description.split()[:50]))
                self.assertNotContains(listing, program.description)
                detail = self.client.get(f"/programs/{program.pk}/")
                for value in (program.name, program.code, program.description, program.coordinator_name, program.coordinator_contact):
                    self.assertContains(detail, value)
                for discipline in program.disciplines.splitlines():
                    self.assertContains(detail, discipline)
            for path in ("/programs/999/", "/departments/999/"):
                self.assertEqual(self.client.get(path).status_code, 404)

        check_pages()
        response = self.client.get("/exchange/", {"country": "Польща"})
        self.assertContains(response, "Uniwersytet Warszawski")
        self.assertContains(response, "Uniwersytet Jagielloński")
        self.assertNotContains(response, "KU Leuven")
        self.assertContains(self.client.get("/exchange/", {"country": "невідома"}), "Програм обміну за вибраною країною немає")
        program = ExchangeProgram.objects.get(pk=3)
        for delta, expected in ((-1, True), (0, True), (1, False)):
            with patch("faculty.models.timezone.localdate", return_value=program.deadline + timedelta(days=delta)):
                self.assertEqual(program.is_open, expected)
                response = self.client.get("/exchange/", {"country": "Литва"})
                self.assertContains(response, "Прийом триває" if expected else "Прийом завершено")
        form = modelform_factory(ExchangeProgram, fields=["places"])
        self.assertFalse(form({"places": -1}).is_valid())

        # Після RunSQL таблиця містить рівно початкові поля й незмінені рядки.
        self.migrate_to("0003_exchange_program")
        apps = self.migrate_to("0004_exchange_data")
        historical = apps.get_model("faculty", "ExchangeProgram")
        self.assertEqual({field.name for field in historical._meta.fields}, {
            "id", "university", "languages", "places", "deadline", "description",
        })
        rows = list(historical.objects.order_by("pk").values())
        self.assertEqual([row["university"] for row in rows], [
            "Uniwersytet Warszawski, Польща", "KU Leuven (Бельгія)",
            "Vilnius University, Литва", "Uniwersytet Jagielloński, Польща",
            "University of Tartu - Естонія", "Masaryk University, Чехія",
        ])
        self.assertEqual([row["places"] for row in rows], ["5", "2 місця", "до 4", "3", "2", "1 місце"])
        self.assertEqual([row["languages"] for row in rows], [
            "польська, англійська", "English", "англійська",
            "Польська, Англійська", "англійська, естонська", "англійська",
        ])
        self.assertEqual([row["deadline"] for row in rows], [
            date(2026, 11, 15), date(2026, 12, 1), date(2026, 10, 20),
            date(2026, 11, 15), date(2027, 1, 10), date(2026, 9, 30),
        ])
        self.migrate_to(latest)
        self.assertEqual(list(ExchangeProgram.objects.order_by("pk").values()), original)
        self.assertEqual(list(ExchangeProgram.objects.order_by("pk").values_list("country", flat=True)), [
            "Польща", "Бельгія", "Литва", "Польща", "Естонія", "Чехія",
        ])
        self.assertEqual(list(ExchangeProgram.objects.order_by("pk").values_list("places", flat=True)), [5, 2, 4, 3, 2, 1])
        apps = self.migrate_to("0005_exchange_country")
        historical = apps.get_model("faculty", "ExchangeProgram")
        self.assertEqual(list(historical.objects.order_by("pk").values_list("places", flat=True)), ["5", "2", "до 4", "3", "2", "1"])
        self.assertEqual(historical.objects.get(pk=3).description, rows[2]["description"])
        apps = self.migrate_to("0004_exchange_data")
        self.assertEqual(apps.get_model("faculty", "ExchangeProgram").objects.get(pk=2).university, "KU Leuven, Бельгія")
        self.migrate_to(latest)
        self.assertEqual(list(ExchangeProgram.objects.order_by("pk").values()), original)

        self.migrate_to(None)
        self.assertFalse(any(table.startswith("faculty_") for table in connection.introspection.table_names()))
        self.assertTrue(get_user_model().objects.filter(pk=admin_user.pk).exists())
        self.migrate_to(latest)
        self.assertEqual(list(ExchangeProgram.objects.order_by("pk").values()), original)
        self.assertEqual((Department.objects.count(), Program.objects.count(), Teacher.objects.count()), (6, 4, 10))
        check_pages()
