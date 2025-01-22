from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PerevalSerializer
from .data_handler import DataHandler

class SubmitDataView(APIView):
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pereval_id, error = DataHandler.create_pereval(serializer.validated_data)
                if error:
                    return Response({
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': error,
                        'id': None
                    }, status=500)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Отправлено успешно',
                    'id': pereval_id
                }, status=200)
            except Exception as e:
                return Response({
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e),
                    'id': None
                }, status=500)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
                'id': None
            }, status=400)

# Create your views here.
