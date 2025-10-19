from django.core.management.base import BaseCommand
import random

from django.utils import timezone

from system.models import OperationLog

MODULES = ['系统管理', '用户管理', '镜像管理', '检测管理', '登录']
OPERATORS = ['admin', 'alice', 'bob', 'system']
IPS = ['127.0.0.1', '192.168.1.10', '10.0.0.5', '203.0.113.45']

class Command(BaseCommand):
    help = 'Seed operation logs with example data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50)

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            OperationLog.objects.create(
                module=random.choice(MODULES),
                operator=random.choice(OPERATORS),
                ip=random.choice(IPS),
                operation_content=f"示例操作内容 #{i+1}",
                operation_time=timezone.now() - timezone.timedelta(minutes=random.randint(0, 60*24))
            )
        self.stdout.write(self.style.SUCCESS(f'Created {count} operation logs'))
