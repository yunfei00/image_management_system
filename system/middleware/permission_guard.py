# system/middlewares/permission_guard.py
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from urllib.parse import urlencode

def _is_api_request(request, api_prefixes):
    p = request.path_info
    return any(p.startswith(x) for x in api_prefixes)

def _wants_json(request):
    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('Accept', '')
    )

class AuthzMiddleware:
    """
    统一拦截：
    1) 未登录：页面跳登录；API 返回 401
    2) 已登录：若视图/配置声明了权限 → 校验；不通过页面 403 / API 403
    3) 超级管理员(is_superuser)直通
    仅做“登录 + 兜底权限”，对象级/数据范围请在视图/DRF里实现
    """

    def __init__(self, get_response):
        self.get_response = get_response
        cfg = getattr(settings, 'PERMISSION_GUARD', {})

        # 命名路由白名单（如 system:login）
        self.whitelist_names = set(cfg.get('WHITELIST', set()))
        # 路径前缀白名单（/admin/、/healthz 等）
        self.path_whitelist = tuple(cfg.get('PATH_WHITELIST', ['/admin/', '/healthz', '/favicon.ico']))
        # API 前缀，用于区分 JSON 响应
        self.api_prefixes = tuple(cfg.get('API_PREFIXES', ['/api/']))
        # 路由→权限映射（兜底），优先匹配“完整名”
        self.permission_map = cfg.get('PERMISSION_MAP', {})

        self.static_url = getattr(settings, 'STATIC_URL', '/static/')
        self.media_url = getattr(settings, 'MEDIA_URL', None)

        # 可开关
        self.enabled = cfg.get('ENABLED', True)

    def __call__(self, request):
        if not self.enabled:
            return self.get_response(request)

        path = request.path_info

        # 1) 静态/媒体直通
        if path.startswith(self.static_url) or (self.media_url and path.startswith(self.media_url)):
            return self.get_response(request)

        # 2) 路径白名单直通
        if any(path.startswith(pfx) for pfx in self.path_whitelist):
            return self.get_response(request)

        # 3) 解析命名路由
        try:
            match = resolve(path)
            url_name = match.url_name
            namespaces = getattr(match, 'namespaces', []) or ([match.namespace] if match.namespace else [])
            full_name = ":".join([*namespaces, url_name]) if url_name else None
        except Resolver404:
            # 让下游处理 404
            return self.get_response(request)

        # 4) 命名白名单直通（如登录/注册/退出）
        if full_name and full_name in self.whitelist_names:
            return self.get_response(request)

        # 5) 登录校验
        user = getattr(request, 'user', None)
        if not (user and user.is_authenticated):
            login_url = getattr(settings, 'LOGIN_URL', '/login/')  # 可写 name 或绝对路径
            if request.method in ('GET', 'HEAD') and not _is_api_request(request, self.api_prefixes):
                return redirect(f"{login_url}?{urlencode({'next': request.get_full_path()})}")
            return JsonResponse({'detail': 'unauthorized'}, status=401)

        # 6) 超管直通
        if user.is_superuser:
            return self.get_response(request)

        # 7) 汇总所需权限（视图属性 + 配置映射）
        required = set()

        # 7.1 视图上声明（CBV/FBV 通吃）：permission_required = 'app.codename' 或列表
        view_func = match.func
        view_cls = getattr(view_func, 'view_class', None)
        for holder in (view_cls, view_func):
            if holder and hasattr(holder, 'permission_required'):
                pr = getattr(holder, 'permission_required')
                required |= set(pr if isinstance(pr, (list, tuple, set)) else [pr])

        # 7.2 settings 兜底映射
        if full_name and full_name in self.permission_map:
            required |= set(self.permission_map[full_name])
        elif url_name and url_name in self.permission_map:
            required |= set(self.permission_map[url_name])

        # 8) 若未声明任何权限 → 放行（只要求登录）
        if not required:
            return self.get_response(request)

        # 9) 校验权限
        if all(user.has_perm(p) for p in required):
            return self.get_response(request)

        # 10) 无权限
        if _is_api_request(request, self.api_prefixes) or _wants_json(request):
            return JsonResponse({'detail': 'forbidden', 'required_perms': sorted(required)}, status=403)
        return HttpResponseForbidden('无权限访问该资源')
