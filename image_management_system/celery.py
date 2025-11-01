# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 默认的 settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_management_system.settings')

app = Celery('your_project')

# 使用消息队列（这里使用 Redis）
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()
