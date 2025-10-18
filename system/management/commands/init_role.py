from system.models import Role

default_roles = [
    {"name": "超管", "code": "super_admin", "permissions": {"*": ["*"]}},
    {"name": "项目管理员", "code": "project_admin", "permissions": {"project": ["view", "edit"], "image": ["view", "upload", "delete"], "detection": ["view", "start", "export"]}},
    {"name": "业务承建方", "code": "contractor", "permissions": {"image": ["view", "upload"], "detection": ["view"]}},
    {"name": "审计人员", "code": "auditor", "permissions": {"image": ["view"], "detection": ["view"]}},
]

for r in default_roles:
    Role.objects.get_or_create(code=r["code"], defaults=r)
