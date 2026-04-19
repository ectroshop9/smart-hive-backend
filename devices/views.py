from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device
from users.models import Beekeeper
from .serializers import DeviceSerializer
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer

class RegisterDeviceAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        
        user_id = data.get('user')
        if user_id:
            try:
                beekeeper = Beekeeper.objects.get(user_id=user_id, is_active=True)
            except Beekeeper.DoesNotExist:
                return Response({'error': 'Invalid user_id'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(last_seen=timezone.now())
            return Response({'status': 'registered', 'device_id': serializer.data['device_id']}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckinAPIView(APIView):
    def post(self, request):
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({'error': 'device_id required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            device = Device.objects.get(device_id=device_id)
            device.last_seen = timezone.now()
            device.is_online = True
            device.save()
            return Response({'status': 'checked_in', 'device_id': device_id})
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


class DeviceListView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            devices = Device.objects.filter(user_id=user_id)
        else:
            devices = Device.objects.all()
        
        data = list(devices.values(
            'device_id', 'device_type', 'name', 'user_id', 'parent_id',
            'firmware_version', 'last_seen', 'is_online', 'registered_at'
        ))
        return Response(data)
