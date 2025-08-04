import logging
import time

import redis
from django.conf import settings

logger = logging.getLogger("monitor")


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        redis_conf = getattr(settings, 'RESPONSE_MONITOR_REDIS', {})
        self.redis_client = redis.StrictRedis(
            host=redis_conf.get('HOST', 'localhost'),
            port=redis_conf.get('PORT', 6379),
            db=redis_conf.get('DB', 1),
            password=redis_conf.get('PASSWORD', None),
            decode_responses=True,
        )

        self.max_history = redis_conf.get('MAX_HISTORY', 100)
        self.expire_seconds = redis_conf.get('EXPIRE_SECONDS', 24 * 3600)

    def __call__(self, request):
        request._start_time = time.time()

        response = self.get_response(request)

        if hasattr(request, '_start_time'):
            response_time = time.time() - request._start_time

            key = f"response_time:{request.method}:{request.path}"

            try:
                self.redis_client.lpush(key, response_time)
                self.redis_client.ltrim(key, 0, self.max_history)
                self.redis_client.expire(key, int(self.expire_seconds))
            except redis.RedisError as e:
                logger.error(f"REDIS-ERROR:{e}")

        return response
