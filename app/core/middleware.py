from fastapi import Request
from datetime import datetime

from core.logger import logger


async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds() * 1000
    
    logger.info(
        f"Method={request.method} Path={request.url.path} "
        f"Status={response.status_code} "
        f"ProcessTime={process_time:.2f}ms"
    )
    
    return response