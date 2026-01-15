from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema

from core.utils import report_log
from .serializers import MonitoringEventSerializer

class MonitoringCreateView(APIView):
    """
    View responsável pelo recebimento e registro de eventos
    de monitoramento enviados por dispositivos edge.

    Esta view valida os dados recebidos, persiste o evento
    no banco de dados e registra a operação em log.
    """
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    @extend_schema(
        request=MonitoringEventSerializer,
        responses={201: None, 400: None, 401: None, 500: None},
        description="Recebe eventos de monitoramento enviados por dispositivos edge."
    )
    def post(self, request: Request) -> Response:
        """
        Processa o registro de um evento de monitoramento.

        Responsabilidades:
        - Validar os dados recebidos do dispositivo edge
        - Persistir o evento de monitoramento
        - Registrar logs de sucesso ou falha

        Espera uma requisição multipart/form-data contendo:
            - mac_address
            - detected_class
            - detected_at
            - evidence (arquivo de imagem)

        Returns
        -------
        Response
            - 201 Created: Evento registrado com sucesso
            - 400 Bad Request: Dados inválidos
            - 401 Unauthorized: Usuário não autenticado
            - 500 Internal Server Error: Erro inesperado
        """
        try:
            serializer = MonitoringEventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            event = serializer.save()
            
            report_log(
                user=request.user,
                action="Criar Evento de Monitoramento",
                status="SUCCESS",
                message=f"Evento registrado para MAC {event.mac_address}"
            )
            return Response(
                {"detail": "Evento registrado com sucesso"},
                status=status.HTTP_201_CREATED
            )
            
        except ValidationError as exc:
            report_log(
                user=request.user,
                action="Criar Evento de Monitoramento",
                status="WARNING",
                message=f"Dados inválidos: {exc}"
            )
            return Response(
                exc.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as exc:
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Criar Evento de Monitoramento",
                status="ERROR",
                message=f"Erro inesperado ao criar evento: {str(exc)}"
            )
            return Response(
                {"detail": "Erro interno do servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
