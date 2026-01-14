from django.db import models

class MonitoringEvent(models.Model):
    """
    Model responsável por representar um evento de detecção
    de objeto de risco enviado por um dispositivo edge.

    Cada registro corresponde a uma ocorrência detectada
    pelo sistema edge-risk-monitor, contendo informações
    suficientes para auditoria, rastreabilidade e análise
    posterior em dashboards.
    """
    mac_address = models.CharField(
        max_length=17,
        verbose_name="MAC do Dispositivo",
        help_text="Identificador lógico do dispositivo edge (XX:XX:XX:XX:XX:XX)"
    )
    
    detected_class = models.CharField(
        max_length=100,
        verbose_name="Classe Detectada",
        help_text="Nome do objeto de risco identificado pelo modelo"
    )
    
    detected_at = models.DateTimeField(
        verbose_name="Data/Hora da Detecção",
        help_text="Momento em que o objeto foi detectado no dispositivo edge"
    )
    
    evidence = models.ImageField(
        upload_to="monitoring/evidence/",
        verbose_name="Evidência Visual",
        help_text="Imagem capturada no momento da detecção"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro",
        help_text="Momento em que o evento foi registrado no backend"
    )
    
    def __str__(self) -> str:
        """
        Retorna uma representação legível do evento,
        útil para logs e administração.
        """
        return f"{self.mac_address} | {self.detected_class} | {self.detected_at}"
    
    class Meta:
        verbose_name = "Evento de Monitoramento"
        verbose_name_plural = "Eventos de Monitoramento"
        ordering = ["-detected_at"]
    
    
    
