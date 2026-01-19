from rest_framework import serializers
from monitoring.models import MonitoringEvent


class DashboardEventSerializer(serializers.ModelSerializer):
    """
    Serializer de saída para o dashboard.

    Responsável por serializar eventos de monitoramento para
    consumo pelo dashboard, garantindo que os dados retornados
    estejam prontos para uso pelo frontend desacoplado.

    Ajustes importantes:
    - Converte o campo de imagem em URL ABSOLUTA
    - Evita que o frontend precise conhecer detalhes de infraestrutura
    - Mantém o backend como fonte única de verdade
    """

    mac = serializers.CharField(
        source="mac_address",
        help_text="Endereço MAC do dispositivo edge"
    )

    class_name = serializers.CharField(
        source="detected_class",
        help_text="Classe do objeto de risco detectado"
    )

    datetime = serializers.DateTimeField(
        source="detected_at",
        help_text="Data e hora da detecção do evento"
    )

    image = serializers.SerializerMethodField(
        help_text="URL absoluta da imagem de evidência do evento"
    )

    class Meta:
        """
        Metadados do serializer DashboardEventSerializer.

        Define o modelo de origem e os campos expostos no payload
        final consumido pelo dashboard.
        """
        model = MonitoringEvent
        fields = [
            "mac",
            "class_name",
            "datetime",
            "image",
        ]

    def get_image(self, obj) -> str | None:
        """
        Retorna a URL absoluta da imagem de evidência.

        Este método garante que o frontend receba uma URL completa,
        independentemente de onde esteja sendo executado
        (localhost, container, domínio, etc).

        Parameters
        ----------
        obj : MonitoringEvent
            Instância do evento de monitoramento.

        Returns
        -------
        str | None
            URL absoluta da imagem de evidência, ou None caso
            não exista imagem associada ao evento.
        """
        if not obj.evidence:
            return None

        request = self.context.get("request")

        if request is None:
            # Fallback seguro (não esperado em produção)
            return obj.evidence.url

        return request.build_absolute_uri(obj.evidence.url)