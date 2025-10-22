# admin.py
from django.contrib import admin
from .models import BaseImage, BusinessImage

@admin.register(BaseImage)
class BaseImageAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "image_id", "status", "category", "size", "created_at")
    list_filter = ("status", "category")
    search_fields = ("name", "version", "image_id")

@admin.register(BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "image_id", "project", "detect_status", "approve_status", "size", "created_at")
    list_filter = ("detect_status", "approve_status")
    search_fields = ("name", "version", "image_id")
