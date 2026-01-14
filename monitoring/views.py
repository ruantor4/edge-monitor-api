from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.utils import report_log

from .serializers import MonitoringEventSerializer


class MonitoringCreateView(APIView):
    """
    View responsável por receber eventos de monitoramento enviados
    pelos dispositivos edge.

    Endpoint:
        POST /api/monitoring/
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request) -> Response:
        """
            Recebe e registra um evento de monitoramento.

            Espera uma requisição multipart/form-data contendo:
                - mac_address
                - detected_class
                - detected_at
                - evidence (arquivo de imagem)

            Returns:
                Response:
                    - 201 Created: Evento registrado com sucesso
                    - 400 Bad Request: Dados inválidos
                    - 401 Unauthorized: Não autenticado
        """
        serializer = MonitoringEventSerializer(data=request.data)
        
        if not serializer.is_valid():
            report_log(
                user=request.user,
                action="Criar Evento de Monitoramento",
                status="ERROR",
                message=f"Dados invalidos: {serializer.errors}"
            ) 
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        event = serializer.save()
            
        report_log(
            user=request.user,
            action="Criar Evento de Monitoramento",
            status="SUCCESS",
            message=f"Evento registrado para MAC {event.mac_address} "
        )  
        return Response(
            {"detail": "Evento registrado com sucesso"},
            status=status.HTTP_201_CREATED
        )

