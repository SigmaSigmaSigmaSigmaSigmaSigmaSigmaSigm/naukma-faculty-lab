import re

from django.db import migrations, models


LIMIT_NOTE = "\n\nКількість місць є верхньою межею: до {}."


def normalize_places(apps, schema_editor):
    Program = apps.get_model("faculty", "ExchangeProgram")
    for program in Program.objects.using(schema_editor.connection.alias).all():
        match = re.fullmatch(r"(до\s+)?([0-9]+)(?:\s+місц(?:е|я|ь))?", program.places.strip())
        if not match:
            raise ValueError(f"Невідома кількість місць: {program.places!r}")
        count = int(match[2])
        if count > 2147483647:
            raise ValueError("Кількість місць перевищує діапазон PositiveIntegerField")
        if match[1]:
            program.description += LIMIT_NOTE.format(count)
        program.places = str(count)
        program.save(update_fields=["places", "description"])


def restore_places(apps, schema_editor):
    Program = apps.get_model("faculty", "ExchangeProgram")
    for program in Program.objects.using(schema_editor.connection.alias).all():
        note = LIMIT_NOTE.format(program.places)
        if program.description.endswith(note):
            program.description = program.description[:-len(note)]
            program.places = f"до {program.places}"
        # Суфікси «місце»/«місця» не відновлюються: їх не зберігає числове поле.
        program.save(update_fields=["places", "description"])


class Migration(migrations.Migration):
    dependencies = [("faculty", "0005_exchange_country")]
    operations = [
        migrations.RunPython(normalize_places, restore_places),
        migrations.AlterField(
            model_name="exchangeprogram", name="places",
            field=models.PositiveIntegerField("Кількість місць"),
        ),
    ]
