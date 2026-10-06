from django.shortcuts import get_object_or_404, render

from .models import Department, ExchangeProgram, HomePage, Program


def home(request):
    return render(request, "faculty/home.html", {"page": HomePage.objects.first()})


def programs(request):
    return render(request, "faculty/programs.html", {"programs": Program.objects.all()})


def program_detail(request, pk):
    program = get_object_or_404(Program.objects.select_related("department"), pk=pk)
    return render(request, "faculty/program_detail.html", {"program": program})


def departments(request):
    items = Department.objects.prefetch_related("programs")
    return render(request, "faculty/departments.html", {"departments": items})


def department_detail(request, pk):
    department = get_object_or_404(
        Department.objects.prefetch_related("programs", "teachers"), pk=pk,
    )
    return render(request, "faculty/department_detail.html", {"department": department})


def exchange(request):
    programs = ExchangeProgram.objects.all()
    countries = programs.order_by("country").values_list("country", flat=True).distinct()
    country = request.GET.get("country", "")
    if country:
        programs = programs.filter(country=country)
    return render(request, "faculty/exchange.html", {
        "programs": programs, "countries": countries, "selected_country": country,
    })
