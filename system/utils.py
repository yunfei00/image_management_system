# system/utils.py
def has_perm(user, perm_key):
    if not user or not user.is_authenticated:
        return False
    # 超管短路
    if user.role_links.filter(role__code='super_admin').exists():
        return True
    return user.role_links.filter(role__permissions__key=perm_key).exists()
