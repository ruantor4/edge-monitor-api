from rest_framework import serializers
from monitoring.models import MonitoringEvent

class DashboardEventSerializer(serializers.ModelSerializer):
    """
    Serializer de saída para o dashboard.

    Responsável por serializar eventos de monitoramento para
    consumo pelo dashboard, conforme especificação do PoC.
    """
    mac = serializers.CharField(source="mac_address")
    class_name = serializers.CharField(source="detected_class")
    datetime = serializers.DateTimeField(source="detected_at")
    image = serializers.ImageField(source="evidence")
    
    class Meta:
        model = MonitoringEvent
        fields = [
            "mac",
            "class_name",
            "datetime",
            "image",
        ]