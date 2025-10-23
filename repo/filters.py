import django_filters

from repo.models import Repository


class RepositoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='仓库名称')
    type = django_filters.ChoiceFilter(field_name='type', choices=[('system', '系统'), ('test', '测试'), ('production', '生产')], label='仓库类型')

    class Meta:
        model = Repository
        fields = ['name', 'type']
