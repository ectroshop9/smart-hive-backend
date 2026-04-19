from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorReading
from devices.models import Device
from .serializers import SensorReadingSerializer
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer

class ReadingAPIView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    
    def get_renderers(self):
        # السماح بتحديد الصيغة عبر query parameter: ?format=csv أو ?format=json
        format_param = self.request.query_params.get('format', 'json')
        if format_param == 'csv':
            return [CSVRenderer()]
        return [JSONRenderer()]
    
    def post(self, request):
        data = request.data.copy()
        
        # تحديث last_seen للجهاز
        device_id = data.get('device')
        if device_id:
            try:
                device = Device.objects.get(device_id=device_id)
                device.last_seen = timezone.now()
                device.is_online = True
                device.save()
            except Device.DoesNotExist:
                pass
        
        serializer = SensorReadingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'id': serializer.data['id']}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        device_id = request.query_params.get('device_id')
        limit = int(request.query_params.get('limit', 100))
        
        if device_id:
            readings = SensorReading.objects.filter(device_id=device_id)[:limit]
        else:
            readings = SensorReading.objects.all()[:limit]
            
        serializer = SensorReadingSerializer(readings, many=True)
        return Response(serializer.data)
