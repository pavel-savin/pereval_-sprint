from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerevalSerializer
from .models import Pereval
from .data_handler import DataHandler

class SubmitDataView(APIView):
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
                'id': None
            }, status=400)
        
        # Используем DataHandler для работы с БД
        result = DataHandler.create_pereval(serializer.validated_data)
        
        return Response({
            'status': result['status'],
            'message': result['message'],
            'id': result['id']
        }, status=result['status'])

# Create your views here.
