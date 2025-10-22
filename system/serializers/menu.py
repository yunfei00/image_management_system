from rest_framework import serializers
from system.models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'parent', 'path', 'icon', 'sort',
                  'status', 'visible', 'is_external', 'permission', 'groups']
        extra_kwargs = {
            'groups': {'required': False}
        }

class MenuTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'path', 'icon', 'sort',
                  'status', 'visible', 'is_external', 'permission', 'children']

    def get_children(self, obj):
        qs = obj.children.order_by('sort', 'id')
        return MenuTreeSerializer(qs, many=True).data
