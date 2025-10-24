from django.contrib import admin

from report.models import Report


# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'period', 'created_at', 'project_status', 'department')
    list_filter = ('type', 'project_status', 'department')
    search_fields = ('type', 'period', 'project_status', 'department')
    ordering = ('-created_at',)

admin.site.register(Report, ReportAdmin)

