from django.db import migrations, models


def split_country(apps, schema_editor):
    Program = apps.get_model("faculty", "ExchangeProgram")
    for program in Program.objects.using(schema_editor.connection.alias).all():
        value = program.university
        if value.endswith(")") and " (" in value:
            name, country = value[:-1].rsplit(" (", 1)
        elif "," in value:
            name, country = value.rsplit(",", 1)
        elif " - " in value:
            name, country = value.rsplit(" - ", 1)
        else:
            raise ValueError(f"Не вдалося визначити країну: {value!r}")
        program.university, program.country = name.strip(), country.strip()
        if not program.university or not program.country:
            raise ValueError(f"Порожня назва або країна: {value!r}")
        program.save(update_fields=["university", "country"])


def join_country(apps, schema_editor):
    Program = apps.get_model("faculty", "ExchangeProgram")
    for program in Program.objects.using(schema_editor.connection.alias).all():
        # Назва і країна зберігаються; початкові роздільники нормалізуються до коми.
        program.university = f"{program.university}, {program.country}"
        program.save(update_fields=["university"])


class Migration(migrations.Migration):
    dependencies = [("faculty", "0004_exchange_data")]
    operations = [
        migrations.AddField(
            model_name="exchangeprogram", name="country",
            field=models.CharField("Країна", max_length=100, default=""),
            preserve_default=False,
        ),
        migrations.RunPython(split_country, join_country),
    ]
