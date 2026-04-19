from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Firmware, OTASession
from devices.models import Device
from django.utils import timezone
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer

class CheckFirmwareAPIView(APIView):
    def post(self, request):
        device_id = request.data.get('device_id')
        current_version = request.data.get('current_version')
        
        if not device_id or not current_version:
            return Response({'error': 'device_id and current_version required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            device = Device.objects.get(device_id=device_id)
            device.last_seen = timezone.now()
            device.is_online = True
            device.firmware_version = current_version
            device.save()
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        latest = Firmware.objects.filter(
            device_type=device.device_type,
            is_stable=True
        ).order_by('-uploaded_at').first()
        
        if latest and latest.version != current_version:
            download_url = request.build_absolute_uri(f'/media/{latest.file_path}')
            return Response({
                'has_update': True,
                'version': latest.version,
                'file_size': latest.file_size,
                'checksum': latest.checksum,
                'changelog': latest.changelog,
                'download_url': download_url
            })
        
        return Response({'has_update': False})


class OTAStatusAPIView(APIView):
    def post(self, request):
        device_id = request.data.get('device_id')
        firmware_version = request.data.get('firmware_version')
        status_update = request.data.get('status')
        progress = request.data.get('progress', 0)
        error_message = request.data.get('error_message', '')
        
        if not device_id or not firmware_version:
            return Response({'error': 'device_id and firmware_version required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            device = Device.objects.get(device_id=device_id)
            firmware = Firmware.objects.get(version=firmware_version, device_type=device.device_type)
            
            session, created = OTASession.objects.get_or_create(
                device=device,
                firmware=firmware,
                status__in=['PENDING', 'DOWNLOADING', 'VERIFYING', 'APPLYING'],
                defaults={'status': status_update}
            )
            
            if not created:
                session.status = status_update
                session.progress = progress
                if error_message:
                    session.error_message = error_message
                if status_update in ['SUCCESS', 'FAILED']:
                    session.completed_at = timezone.now()
                    if status_update == 'SUCCESS':
                        device.firmware_version = firmware_version
                        device.save()
                session.save()
            
            device.last_seen = timezone.now()
            device.is_online = True
            device.save()
            
            return Response({
                'status': 'updated',
                'session_id': session.id,
                'device_firmware': device.firmware_version
            })
            
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        except Firmware.DoesNotExist:
            return Response({'error': 'Firmware version not found'}, status=status.HTTP_404_NOT_FOUND)


class FirmwareListView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    
    def get(self, request):
        firmwares = Firmware.objects.all()
        data = list(firmwares.values(
            'firmware_id', 'version', 'device_type', 
            'file_size', 'is_stable', 'uploaded_at'
        ))
        return Response(data)
