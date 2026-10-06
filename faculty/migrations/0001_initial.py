from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    # Відкат видаляє таблиці першої частини разом з їхнім вмістом.
    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField("Назва", max_length=200)),
                ("head", models.CharField("Завідувач кафедри", max_length=200)),
            ],
            options={"verbose_name": "Кафедра", "verbose_name_plural": "Кафедри", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="HomePage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField("Заголовок", max_length=200)),
                ("description", models.TextField("Опис та основна інформація")),
                ("contacts", models.TextField("Контакти")),
            ],
            options={"verbose_name": "Головна сторінка", "verbose_name_plural": "Головна сторінка"},
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField("Назва", max_length=200)),
                ("code", models.CharField("Код", max_length=20)),
                ("description", models.TextField("Опис")),
                ("coordinator_name", models.CharField("Ім’я координатора набору", max_length=200)),
                ("coordinator_contact", models.CharField("Контакт координатора набору", max_length=200)),
                ("disciplines", models.TextField("Дисципліни", help_text="Кожна дисципліна з нового рядка.")),
                ("department", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="programs", to="faculty.department", verbose_name="Випускова кафедра")),
            ],
            options={"verbose_name": "Спеціальність", "verbose_name_plural": "Спеціальності", "ordering": ["code", "name"]},
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField("Ім’я", max_length=200)),
                ("position", models.CharField("Посада", max_length=200)),
                ("degree", models.CharField("Науковий ступінь", max_length=200)),
                ("department", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="teachers", to="faculty.department", verbose_name="Кафедра")),
            ],
            options={"verbose_name": "Викладач", "verbose_name_plural": "Викладачі", "ordering": ["name"]},
        ),
    ]
