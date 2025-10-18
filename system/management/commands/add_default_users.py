from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from system.models_all import User, Department  # 导入你的User和Department模型


class Command(BaseCommand):
    help = "添加默认用户信息（关联已存在的部门，角色为空）"

    def handle(self, *args, **options):
        # 定义默认用户数据：用户名、密码、部门名称（需提前在数据库中存在）
        default_users = [
            {
                "username": "admin",
                "password": "admin123",  # 实际使用时建议修改为复杂密码
                "email": "admin@example.com",
                "phone": "13800138000",
                "department": "总部"  # 关联已存在的“总部”部门
            },
            {
                "username": "tech_user",
                "password": "tech123",
                "email": "tech@example.com",
                "phone": "13900139000",
                "department": "技术部"  # 关联已存在的“技术部”部门
            },
            {
                "username": "market_user",
                "password": "market123",
                "email": "market@example.com",
                "phone": "13700137000",
                "department": "市场部"  # 关联已存在的“市场部”部门
            }
        ]

        for user_data in default_users:
            # 查找对应的部门（根据部门名称）
            try:
                department = Department.objects.get(name=user_data["department"])

                print('department', department.name)
            except Department.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"部门 '{user_data['department']}' 不存在，请先添加该部门再执行命令！"
                ))
                continue  # 跳过该用户，处理下一个

            # 检查用户是否已存在（避免重复创建）
            username = user_data["username"]
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"用户 '{username}' 已存在，跳过创建。"))
                continue

            # 创建用户（角色role设为None，即空）
            print('fuck here')

            user = User.objects.create(
                username=username,
                password=make_password(user_data["password"]),  # 密码加密存储
                email=user_data["email"],
                phone=user_data["phone"],
                department=department,  # 关联部门
                role=None,  # 角色为空
                status=1  # 状态设为“启用”（1=启用，0=停用，根据你的模型定义调整）
            )
            exit()
            self.stdout.write(self.style.SUCCESS(f"成功创建用户：{username}（部门：{department.name}）"))

        self.stdout.write(self.style.SUCCESS("默认用户添加完成！"))