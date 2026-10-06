from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("programs/", views.programs, name="programs"),
    path("programs/<int:pk>/", views.program_detail, name="program_detail"),
    path("departments/", views.departments, name="departments"),
    path("departments/<int:pk>/", views.department_detail, name="department_detail"),
    path("exchange/", views.exchange, name="exchange"),
]
