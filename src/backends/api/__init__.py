from fastapi import APIRouter
from .endpoints import for_eval 
from .endpoints import for_service
# 라우터 생성
eval_router = APIRouter()

eval_router.include_router(
    for_eval.app.router, 
    prefix="/for_eval",      
    tags=["eval"]       
) 

service_router = APIRouter()

service_router.include_router(
    for_service.app.router,
    prefix = "/for_service",
    tags = ["service"]
)