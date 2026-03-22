import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uad_audit")

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        client_ip = request.client.host if request.client else "Unknown"
        method = request.method
        url = request.url.path
        status_code = response.status_code
        
        api_key = request.headers.get("x-api-key", "None provided")
        # Mask API key for security log
        masked_key = f"{api_key[:8]}***" if len(api_key) > 8 else "None"
        
        logger.info(
            f"AUDIT | IP: {client_ip} | Method: {method} | Path: {url} | "
            f"Status: {status_code} | Duration: {process_time:.4f}s | Key: {masked_key}"
        )
        
        return response
