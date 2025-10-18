# system/utils.py
from openpyxl import Workbook
from django.http import HttpResponse
import datetime


def has_perm(user, perm_key):
    if not user or not user.is_authenticated:
        return False
    # 超管短路
    if user.role_links.filter(role__code='super_admin').exists():
        return True
    return user.role_links.filter(role__permissions__key=perm_key).exists()


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