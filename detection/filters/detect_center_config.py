import django_filters
from detection.models import DetectCenterConfig, DetectDevice

class DetectCenterConfigFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='配置名称')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact', label='状态')

    class Meta:
        model = DetectCenterConfig
        fields = ['status', 'name']

class DetectDeviceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='设备名称')
    type = django_filters.CharFilter(field_name='type', lookup_expr='icontains', label='设备类型')
    api_url = django_filters.CharFilter(field_name='api_url', lookup_expr='icontains', label='API地址')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact', label='状态')

    class Meta:
        model = DetectDevice
        fields = ['status', 'name', 'type', 'api_url']
