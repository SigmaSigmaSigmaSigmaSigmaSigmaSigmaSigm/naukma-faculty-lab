from django.contrib import admin

from .models import Department, ExchangeProgram, HomePage, Program, Teacher


admin.site.register([Department, Program, Teacher, ExchangeProgram])


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return super().has_add_permission(request) and not HomePage.objects.exists()
