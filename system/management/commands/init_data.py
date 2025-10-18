# 文件路径：apps/system/management/commands/init_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from system.models_all import Department, Role  # 按实际app名称调整
from django.db import transaction

class Command(BaseCommand):
    help = "初始化系统基础数据（部门、角色、用户）"

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        # 1️⃣ 创建部门
        root_dept, _ = Department.objects.get_or_create(name="总部", parent=None)
        dev_dept, _ = Department.objects.get_or_create(name="开发部", parent=root_dept)
        ops_dept, _ = Department.objects.get_or_create(name="运维部", parent=root_dept)

        self.stdout.write(self.style.SUCCESS("✅ 部门初始化完成"))

        # 2️⃣ 创建角色
        super_role, _ = Role.objects.get_or_create(name="超级管理员", code="admin")
        manager_role, _ = Role.objects.get_or_create(name="管理方", code="mgm")
        business_role, _ = Role.objects.get_or_create(name="业务方", code="bus")
        ops_role, _ = Role.objects.get_or_create(name="运维", code="developer")
        construction_role, _ = Role.objects.get_or_create(name="承建方", code="ops")

        self.stdout.write(self.style.SUCCESS("✅ 角色初始化完成"))

        # 3️⃣ 创建用户
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin",
                password="admin123",
                phone="13800000000",
                department=root_dept,
            )
            # admin_user.roles.add(super_role)
            self.stdout.write(self.style.SUCCESS("✅ 管理员用户已创建：admin / admin123"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ 管理员用户已存在，跳过创建"))

        if not User.objects.filter(username="user").exists():
            dev_user = User.objects.create_user(
                username="user",
                password="123456",
                department=dev_dept,
                phone="13811111111",
            )
            # dev_user.roles.add(super_role)
            self.stdout.write(self.style.SUCCESS("✅ 开发用户已创建：user / 123456"))

        if not User.objects.filter(username="李四").exists():
            ops_user = User.objects.create_user(
                username="李四",
                password="123456",
                name="李四",
                department=ops_dept,
                phone="13822222222",
            )
            # ops_user.role.add(ops_role)
            self.stdout.write(self.style.SUCCESS("✅ 运维用户已创建：李四 / 123456"))
