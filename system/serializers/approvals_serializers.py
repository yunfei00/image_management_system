# apps/approvals/serializers.py
from rest_framework import serializers
from system.models import ApprovalFlow

class ApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalFlow
        fields = ["id", "name", "nodes_config", "status", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        nodes = attrs.get("nodes_config") or {}
        # 最基本的合法性校验：必须包含非空的 nodes 数组
        if not isinstance(nodes, dict) or not isinstance(nodes.get("nodes"), list) or len(nodes["nodes"]) == 0:
            raise serializers.ValidationError({"nodes_config": "必须包含至少一个审批节点（nodes: []）。"})
        return attrs
