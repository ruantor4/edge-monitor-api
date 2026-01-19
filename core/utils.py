from core.models import LogSystem
from django.contrib.auth.models import AnonymousUser

def report_log(
    user,
    action: str,
    status: str,
    message: str  
) -> None:
    """
    Registra um evento de log no sistema.

    Esta função centraliza a criação de registros no modelo LogSystem,
    sendo utilizada por diferentes camadas da aplicação para registrar
    ações relevantes para auditoria, rastreabilidade e diagnóstico.

    O parâmetro `user` é normalizado para garantir que usuários
    anônimos ou valores inválidos não causem falhas na persistência
    do registro.

    Parameters
    ----------
    user
        Instância do usuário autenticado responsável pela ação,
        ou None quando a ação não estiver associada a um usuário.
    action : str
        Identificador textual da ação executada.
    status : str
        Status da ação (ex.: SUCCESS, WARNING, ERROR).
    message : str
        Descrição detalhada do evento registrado.

    Returns
    -------
    None
        Esta função não retorna valores.
    """
    
    # Normaliza o usuário para evitar inconsistências
    if not user or isinstance(user, AnonymousUser):
        user = None
    
    # Persiste o log no banco de dados   
    LogSystem.objects.create(
        user = user,
        action = action,
        status = status,
        message = message
    )