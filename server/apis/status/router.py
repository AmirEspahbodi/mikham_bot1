from fastapi import APIRouter, Request

from core.config import RedisConfig, AppConfig
from utils import (
    get_neshan_not_imported_requests,
    get_google_map_imported_requests,
    get_google_map_not_imported_requests,
    get_neshan_imported_requests,
)
from .schema import ResponseBody
from core.connection import redis


status_router = APIRouter()
from pydantic import BaseModel, Field


@status_router.get("/status", response_model=ResponseBody, status_code=200)
async def question(request: Request):
    """
    get scrap status
    """
    
    google_map_in_processing_requests = redis.get(
        RedisConfig.REDIS_GOOGLE_MAP_IN_PROCESSING_SEARCH_QUERY
    )
    google_map_sleeped_search_requests = redis.lrange(
        RedisConfig.REDIS_SLEEP_GOOGLE_MAP_SEARCH_QUERIES, start=0, end=-1,
    )
    google_map_in_queue_search_queries = redis.lrange(
        RedisConfig.REDIS_INQUEUE_GOOGLE_MAP_SEARCH_QUERIES, start=0, end=-1,
    )
    google_map_imported_requests = get_google_map_imported_requests()
    google_map_not_imported_requests = get_google_map_not_imported_requests()
    
    neshan_in_processing_requests = redis.get(
        RedisConfig.REDIS_NESHAN_IN_PROCESSING_SEARCH_QUERY
    )
    neshan_sleeped_search_requests = redis.lrange(
        RedisConfig.REDIS_SLEEP_NESHAN_SEARCH_QUERIES, start=0, end=-1,
    )
    neshan_in_queue_search_queries = redis.lrange(
        RedisConfig.REDIS_INQUEUE_NESHAN_SEARCH_QUERIES, start=0, end=-1,
    )
    neshan_imported_requests = get_neshan_imported_requests()
    neshan_not_imported_requests = get_neshan_not_imported_requests()    
    

    return {
        "google_map_in_processing_requests": google_map_in_processing_requests,
        "google_map_sleeped_search_requests": google_map_sleeped_search_requests,
        "google_map_in_queue_search_queries": google_map_in_queue_search_queries,
        "google_map_imported_requests": google_map_imported_requests,
        "google_map_not_imported_requests": google_map_not_imported_requests,
        "neshan_in_processing_requests": neshan_in_processing_requests,
        "neshan_sleeped_search_requests": neshan_sleeped_search_requests,
        "neshan_in_queue_search_queries": neshan_in_queue_search_queries,
        "neshan_imported_requests": neshan_imported_requests,
        "neshan_not_imported_requests": neshan_not_imported_requests,
    }
