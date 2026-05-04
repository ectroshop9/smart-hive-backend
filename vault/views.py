import os, json, hashlib, time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Block
from .crypto_engine.decryptor import CryptoEngine

crypto = CryptoEngine()

@csrf_exempt
def ingest(request):
    if request.method != 'POST':
        return JsonResponse({"status": "ERROR", "message": "POST only"}, status=405)
    try:
        content = json.loads(request.body)
        payload = content.get('payload', '')
        signature = content.get('signature', '')
        mac = content.get('mac', 'UNKNOWN')
        nonce = content.get('nonce', None)
        
        result = crypto.decrypt_data(payload, signature, mac, nonce)
        if result['status'] == 'REJECTED':
            return JsonResponse(result, status=403)
        
        ts = int(time.time())
        last = Block.objects.filter(mac=mac).order_by('-id').first()
        previous_hash = last.block_hash if last else "0"*64
        
        data_json = json.dumps(result['data'])
        block_content = f"{mac}|{previous_hash}|{data_json}|{nonce}|{ts}"
        block_hash = hashlib.sha256(block_content.encode()).hexdigest()
        
        block = Block.objects.create(
            mac=mac, previous_hash=previous_hash, block_hash=block_hash,
            data_json=data_json, signature_b64=signature, nonce=nonce, timestamp=ts
        )
        
        return JsonResponse({
            "status": "SECURED", "blockchain_hash": block_hash,
            "block_id": block.id, "previous_hash": previous_hash,
            "data": result['data']
        }, status=201)
    except Exception as e:
        return JsonResponse({"status": "ERROR", "message": str(e)}, status=500)

def verify(request):
    block_hash = request.GET.get('hash', '')
    if not block_hash:
        return JsonResponse({"status": "ERROR", "message": "Missing hash"}, status=400)
    try:
        block = Block.objects.get(block_hash=block_hash)
        return JsonResponse({
            "status": "VERIFIED", "verified": True,
            "block_hash": block.block_hash, "mac": block.mac,
            "previous_hash": block.previous_hash,
            "data": json.loads(block.data_json),
            "nonce": block.nonce, "timestamp": block.timestamp
        })
    except Block.DoesNotExist:
        return JsonResponse({"status": "NOT_FOUND", "verified": False}, status=404)

def chain(request):
    mac = request.GET.get('mac')
    limit = int(request.GET.get('limit', 50))
    qs = Block.objects.filter(mac=mac) if mac else Block.objects.all()
    blocks = qs.order_by('-id')[:limit]
    return JsonResponse({
        "chain": [{"hash": b.block_hash, "previous": b.previous_hash,
                   "mac": b.mac, "nonce": b.nonce, "timestamp": b.timestamp} for b in blocks],
        "count": len(blocks)
    })

def health(request):
    return JsonResponse({"status": "ALIVE", "system": "al_baraka_vault", "version": "4.0"})
