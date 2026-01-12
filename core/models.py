from django.db import models
from django.conf import settings


class LogSystem(models.Model):
    """
    Model responsável por armazenar registros de operações realizadas no sistema.

    Este modelo é utilizado para persistir logs de auditoria e rastreabilidade,
    registrando ações executadas por usuários autenticados ou eventos gerados
    pelo próprio sistema. Os registros aqui armazenados não devem ser removidos
    automaticamente, garantindo histórico completo para análise e depuração.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        verbose_name = "Usuário"                
    )
    
    action = models.CharField(
        max_length = 255,
        verbose_name = "Ação"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Data e Hora"
    )
    
    status = models.CharField(
        max_length = 100,
        verbose_name = "Status"
    )
    
    message = models.TextField(
        verbose_name = "Mensagem"
    )
    
    def __str__(self) -> str:
        """
        Retorna uma representação legível do registro de log,
        combinando data/hora, usuário (quando existir) e ação registrada.

        Returns
        -------
        str
            String representativa do log para exibição administrativa.
        """
        user = self.user.username if self.user else "Anônimo"
        return f"{self.timestamp} - {user} - {self.action}"
    
    class Meta:
        """
        Metadados do model LogSystem.

        Define o nome da tabela no banco de dados, a ordenação padrão
        dos registros e os nomes legíveis utilizados na interface administrativa.
        """
        db_table = "log_system"
        ordering = ["-timestamp"]
        verbose_name = "Log do Sistema"
        verbose_name_plural = "Logs do Sistema"