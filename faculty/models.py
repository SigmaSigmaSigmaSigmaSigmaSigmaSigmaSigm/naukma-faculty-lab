from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField("Назва", max_length=200)
    head = models.CharField("Завідувач кафедри", max_length=200)

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедри"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField("Назва", max_length=200)
    code = models.CharField("Код", max_length=20)
    description = models.TextField("Опис")
    coordinator_name = models.CharField("Ім’я координатора набору", max_length=200)
    coordinator_contact = models.CharField("Контакт координатора набору", max_length=200)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="programs",
        verbose_name="Випускова кафедра",
    )
    disciplines = models.TextField("Дисципліни", help_text="Кожна дисципліна з нового рядка.")

    class Meta:
        verbose_name = "Спеціальність"
        verbose_name_plural = "Спеціальності"
        ordering = ["code", "name"]

    def __str__(self):
        return f"{self.code} — {self.name}"


class Teacher(models.Model):
    name = models.CharField("Ім’я", max_length=200)
    position = models.CharField("Посада", max_length=200)
    degree = models.CharField("Науковий ступінь", max_length=200)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="teachers",
        verbose_name="Кафедра",
    )

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ["name"]

    def __str__(self):
        return self.name


class HomePage(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Опис та основна інформація")
    contacts = models.TextField("Контакти")

    class Meta:
        verbose_name = "Головна сторінка"
        verbose_name_plural = "Головна сторінка"

    def __str__(self):
        return self.title


class ExchangeProgram(models.Model):
    university = models.TextField("Університет")
    country = models.CharField("Країна", max_length=100)
    languages = models.TextField("Мови навчання")
    places = models.PositiveIntegerField("Кількість місць")
    deadline = models.DateField("Дедлайн подачі")
    description = models.TextField("Опис")

    class Meta:
        verbose_name = "Програма обміну"
        verbose_name_plural = "Програми обміну"
        ordering = ["deadline", "university"]

    @property
    def is_open(self):
        return timezone.localdate() <= self.deadline

    def __str__(self):
        return self.university
