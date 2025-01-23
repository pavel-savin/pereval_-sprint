from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from .serializers import PerevalSerializer
from .models import Pereval
from .data_handler import DataHandler
from decouple import config


class PerevalDetailView(RetrieveAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"status": 404, "message": str(e), "id": None},
                status=status.HTTP_404_NOT_FOUND
            )
class PerevalUpdateView(UpdateAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['patch']
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.status != 'new':
                return Response(
                    {"state": 0, "message": "Редактирование запрещено: запись не в статусе 'new'"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if 'user' in request.data:
                return Response(
                    {"state": 0, "message": "Редактирование данных пользователя запрещено"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response({"state": 1, "message": None}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"state": 0, "message": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def perform_update(self, serializer):
        serializer.save(status='pending')
        
class PerevalListView(ListAPIView):
    serializer_class = PerevalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return Pereval.objects.all()
    
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
