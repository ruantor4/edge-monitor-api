from rest_framework import serializers

from .models import MonitoringEvent

class MonitoringEventSerializer(serializers.ModelSerializer):
    """
    Serializer responsável por validar e criar eventos de monitoramento
    enviados pelos dispositivos edge.

    Este serializer recebe dados estruturados via multipart/form-data,
    incluindo campos textuais e um arquivo de imagem de evidência.
    """
    class Meta:
        model = MonitoringEvent
        fields = [
            "mac_address",
            "detected_class",
            "detected_at",
            "evidence",
        ]
        
    def validate_mac_address(self, value: str) -> str:
        """
        Valida o formato do endereço MAC lógico do dispositivo edge.

        Args:
            value (str): MAC enviado pelo edge.

        Returns:
            str: MAC validado.
        """
        if len(value) != 17:
            raise serializers.ValidationError(
                "MAC address inválido. Formato esperado XX:XX:XX:XX:XX:XX"
            )
        return value.upper()
    