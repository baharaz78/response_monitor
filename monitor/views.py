import redis
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_middleware(request):
    try:
        redis_conf = getattr(settings, 'RESPONSE_MONITOR_REDIS', {})
        redis_client = redis.StrictRedis(
            host=redis_conf.get('REDIS_HOST', 'localhost'),
            port=redis_conf.get('REDIS_PORT', 6379),
            db=redis_conf.get('REDIS_DB', 1),
            password=redis_conf.get('REDIS_PASSWORD', None),
            decode_responses=True,
        )

        key = f"response_time:{request.method}:{request.path}"
        times = redis_client.lrange(key, 0, 4)
        count = redis_client.llen(key)

    except:
        times = []
        count = 0

    return JsonResponse({
        'message': 'Response Time Monitor',
        'redis_data': {
            'key': f"response_time:{request.method}:{request.path}",
            'total_requests': count,
            'last_5_times': times
        }
    })
