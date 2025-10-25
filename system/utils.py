# system/utils.py
from openpyxl import Workbook
from django.http import HttpResponse
import datetime
from collections import OrderedDict

def require_perms(*perms):
    def deco(func_or_cls):
        setattr(func_or_cls, 'permission_required', perms)
        return func_or_cls
    return deco

def has_perm(user, perm_key):
    if not user or not user.is_authenticated:
        return False
    # 超管短路
    if user.role_links.filter(role__code='super_admin').exists():
        return True
    return user.role_links.filter(role__permissions__key=perm_key).exists()



def custom_attrs(obj):
    out = OrderedDict()
    # 1) 实例级属性（你在 __init__ 或运行时 set 的）
    for k, v in vars(obj).items():         # 等价于 obj.__dict__，但更安全
        if not k.startswith('_'):
            out[k] = v

    # 2) 类级属性与 @property（非方法、非内置）
    for k, v in obj.__class__.__dict__.items():
        if k.startswith('_') or k in out:
            continue
        if isinstance(v, property):
            try:
                out[k] = getattr(obj, k)   # 访问 property 值
            except Exception as e:
                out[k] = f"<property error: {e}>"
        elif not callable(v):              # 排除方法
            out[k] = v

    return out

def print_custom_attrs(obj):
    for k, v in custom_attrs(obj).items():
        print(f"{k} = {v!r}")

def print_objs(objs):
    for obj in objs:
        print_custom_attrs(obj)



def export_queryset_to_excel(queryset, columns, filename_prefix='export'):
    wb = Workbook()
    ws = wb.active
    ws.append([col[1] for col in columns])  # header labels
    for obj in queryset:
        row = []
        for field_name, _label in columns:
            val = getattr(obj, field_name)
            # for ManyToMany fields, show comma-separated names
            try:
                if hasattr(val, 'all'):
                    row.append(", ".join([str(i) for i in val.all()]))
                else:
                    row.append(str(val) if val is not None else "")
            except Exception:
                row.append(str(val))
        ws.append(row)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"{filename_prefix}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response