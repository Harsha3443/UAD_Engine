from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
from typing import Dict
import hashlib

# Simple in-memory rate limiting
rate_limit_records: Dict[str, list] = {}
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("x-api-key")
        
        if api_key:
            api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            current_time = time.time()
            
            if api_key_hash not in rate_limit_records:
                rate_limit_records[api_key_hash] = []
                
            rate_limit_records[api_key_hash] = [
                t for t in rate_limit_records[api_key_hash] 
                if current_time - t < RATE_LIMIT_WINDOW
            ]
            
            if len(rate_limit_records[api_key_hash]) >= RATE_LIMIT_REQUESTS:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Try again later."}
                )
                
            rate_limit_records[api_key_hash].append(current_time)
            
        return await call_next(request)
