from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("faculty", "0002_faculty_content")]
    # Відкат видаляє таблицю та всі програми, зокрема додані після міграції.
    operations = [
        migrations.CreateModel(
            name="ExchangeProgram",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("university", models.TextField("Університет")),
                ("languages", models.TextField("Мови навчання")),
                ("places", models.TextField("Кількість місць")),
                ("deadline", models.DateField("Дедлайн подачі")),
                ("description", models.TextField("Опис")),
            ],
            options={"verbose_name": "Програма обміну", "verbose_name_plural": "Програми обміну", "ordering": ["deadline", "university"]},
        ),
    ]
