from core.models import LogSystem
from django.contrib.auth.models import AnonymousUser

def report_log(
    user,
    action: str,
    status: str,
    message: str  
) -> None:
    """
    Registra uma entrada de log no sistema.

    Esta função é responsável por criar registros no modelo LogSystem,
    armazenando informações sobre ações executadas por usuários
    autenticados, usuários anônimos ou pelo próprio sistema.

    A função garante que inconsistências no parâmetro `user` não
    provoquem falhas durante a persistência do log.
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