from rest_framework import serializers
from .models import MonitoringEvent

class MonitoringEventSerializer(serializers.ModelSerializer):
    """
    Serializer responsável por validar e criar eventos de monitoramento.

    Este serializer atua como camada de validação dos dados recebidos
    dos dispositivos edge, garantindo a integridade e o formato correto
    das informações antes da persistência no banco de dados.
    """
    class Meta:
        """
        Metadados do serializer MonitoringEventSerializer.

        Define o modelo associado e os campos obrigatórios para
        criação de um evento de monitoramento.
        """
        model = MonitoringEvent
        fields = [
            "mac_address",
            "detected_class",
            "detected_at",
            "evidence",
        ]

    def validate_mac_address(self, value: str) -> str:
        """
        Valida o formato do endereço MAC informado.

        Este método garante que o valor informado possua o tamanho
        esperado de um endereço MAC e normaliza o conteúdo para
        letras maiúsculas.

        Parameters
        ----------
        value : str
            Endereço MAC recebido na requisição.

        Returns
        -------
        str
            Endereço MAC validado e normalizado.

        Raises
        ------
        serializers.ValidationError
            Caso o formato do endereço MAC seja inválido.
        """
        if len(value) != 17:
            raise serializers.ValidationError(
                "MAC address inválido. Formato esperado XX:XX:XX:XX:XX:XX"
            )
        return value.upper()
