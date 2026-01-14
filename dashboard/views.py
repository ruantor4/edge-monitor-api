from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.utils import report_log
from monitoring.models import MonitoringEvent
from .serializers import DashboardEventSerializer


class DashboardView(APIView):
    """
    View responsável por fornecer dados para o dashboard.

    Endpoint:
        GET /api/dashboard?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """
        Retorna eventos de monitoramento filtrados por intervalo de datas.

        Query params:
            - start_date (YYYY-MM-DD)
            - end_date (YYYY-MM-DD)

        Returns:
            Response:
                - 200 OK: Lista de eventos
                - 400 Bad Request: Parâmetros inválidos
        """
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        if not start_date or not end_date:
            return Response(
                {"detail": "Parâmetros start_date e end_date são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            
            end_date = end_date.replace(hour=23, minute=59, second=59)
        
        except ValueError:
            return Response(
                {"detail": "Formato de data inválido. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        events = MonitoringEvent.objects.filter(
            detected_at__range=(start_date, end_date)
        ).order_by("-detected_at")
        
        serializer = DashboardEventSerializer(events, many=True)
        
        report_log(
            user=request.user if request.user.is_authenticated else None,
            action="Consultar Dashboard",
            status="INFO",
            message=f"{events.count()} eventos retornados no dashboard"
        )
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )