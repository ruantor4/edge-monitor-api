from rest_framework import serializers
from .models import MonitoringEvent

class MonitoringEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringEvent
        fields = [
            "mac_address",
            "detected_class",
            "detected_at",
            "evidence",
        ]

    def validate_mac_address(self, value: str) -> str:
        if len(value) != 17:
            raise serializers.ValidationError(
                "MAC address inválido. Formato esperado XX:XX:XX:XX:XX:XX"
            )
        return value.upper()
