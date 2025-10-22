# images/filters.py
import django_filters as df
from .models import BaseImage, BusinessImage

class BaseImageFilter(df.FilterSet):
    # 关键字段做模糊查询
    name = df.CharFilter(field_name='name', lookup_expr='icontains', label='镜像名称')
    version = df.CharFilter(field_name='version', lookup_expr='icontains', label='版本')
    image_id = df.CharFilter(field_name='image_id', lookup_expr='icontains', label='镜像ID')

    class Meta:
        model = BaseImage
        # 其余用默认 exact 查询，保持简单
        fields = ['status', 'category', 'name', 'version', 'image_id']


class BusinessImageFilter(df.FilterSet):
    # 关键字段做模糊查询
    name = df.CharFilter(field_name='name', lookup_expr='icontains', label='镜像名称')
    version = df.CharFilter(field_name='version', lookup_expr='icontains', label='版本')
    image_id = df.CharFilter(field_name='image_id', lookup_expr='icontains', label='镜像ID')
    # 项目按 ID 精确匹配（保持最简）
    project = df.NumberFilter(field_name='project_id', label='项目ID')

    class Meta:
        model = BusinessImage
        fields = ['detect_status', 'approve_status', 'project', 'name', 'version', 'image_id']
