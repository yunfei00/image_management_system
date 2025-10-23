from django.contrib import admin

from detection.models import DetectTool, ProjectDetectTool, PreDetectRecord


# Register your models here.

@admin.register(DetectTool)
class DetectToolAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "status", "last_test_time", "created_at")
    list_filter = ("type", "status")
    search_fields = ("name",)

@admin.register(ProjectDetectTool)
class ProjectDetectToolAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "tool", "available", "updated_at")
    list_filter = ("available", "tool__type", "tool__status")
    search_fields = ("project__name", "tool__name")

@admin.register(PreDetectRecord)
class PreDetectRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "tool", "status", "vulnerability_count", "detect_time", "created_at")
    list_filter = ("status", "tool", "project")
    search_fields = ("project__name", "tool__name", "request_id")
    date_hierarchy = "detect_time"
