from fastapi import APIRouter, HTTPException, status
from .schema import RequestBody, ResponseBody
from core.connection import redis
from core.config import RedisConfig
from utils import (
    get_neshan_not_imported_requests,
    get_google_map_imported_requests,
    get_google_map_not_imported_requests,
    get_neshan_imported_requests,
)
from core.config import AppConfig

scrap_req_router = APIRouter()


@scrap_req_router.post(
    "/request_in_google_map", response_model=ResponseBody, status_code=200
)
async def request(body: RequestBody):
    """
    request search query to scrap in google map
    """
    sleeped_search_requests: list[str] = redis.lrange(
        name=RedisConfig.REDIS_SLEEP_GOOGLE_MAP_SEARCH_QUERIES,
        start=0,
        end=-1,
    )
    in_queue_search_queries: list[str] = redis.lrange(
        name=RedisConfig.REDIS_INQUEUE_GOOGLE_MAP_SEARCH_QUERIES,
        start=0,
        end=-1,
    )
    in_processing_requests: str = redis.get(
        RedisConfig.REDIS_GOOGLE_MAP_IN_PROCESSING_SEARCH_QUERY
    )

    imported_requests = get_google_map_imported_requests()
    not_imported_requests = get_google_map_not_imported_requests()

    error_message = ""

    requested_search_query = (
        f"{body.listing_type.strip()}"
        + f"{AppConfig.SEARCH_QUERY_SEPARATOR.strip()}"
        + f"{body.verb.strip()}"
        + f"{AppConfig.SEARCH_QUERY_SEPARATOR.strip()}"
        + f"{body.city.strip()}"
    )
    clean_requested_search_query = (
        f"{body.listing_type.strip()}"
        + f" "
        + f"{body.verb.strip()}"
        + f" "
        + f"{body.city.strip()}"
    )

    if imported_requests:
        for imported_request in imported_requests:
            listing_category, listing_search_query, province, scraper = [
                i.strip()
                for i in imported_request.split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is imported to site under type of {listing_category}"

    if not_imported_requests:
        for not_imported_request in not_imported_requests:
            listing_category, listing_search_query, province, scraper = [
                i.strip()
                for i in not_imported_request.split(
                    AppConfig.LISTING_NAME_ITEMS_SEPARATOR
                )
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is scraped (but not imported to site) under type of {listing_category}"

    if sleeped_search_requests:
        for sleeped_request in sleeped_search_requests:
            listing_category, listing_search_query, province = [
                i.strip()
                for i in sleeped_request.split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is sleeped and waiting to enter on scraper queue under type of {listing_category}"
    if in_queue_search_queries:
        for in_queue_search_query in in_queue_search_queries:
            listing_category, listing_search_query, province = [
                i.strip()
                for i in in_queue_search_query.split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is in scraper queue under type of {listing_category}"
        
    
    if in_processing_requests:
        listing_category, listing_search_query, province = [
            i.strip()
            for i in in_processing_requests.split(
                AppConfig.LISTING_NAME_ITEMS_SEPARATOR
            )
        ]
        if requested_search_query == listing_search_query:
            error_message = f"The {clean_requested_search_query} request is being scrapped. under type of {listing_category}"

    if error_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )

    search_query = (
        f"{body.listing_category.strip()}"
        + f"{AppConfig.LISTING_NAME_ITEMS_SEPARATOR.strip()}"
        + f"{requested_search_query}"
        + f"{AppConfig.LISTING_NAME_ITEMS_SEPARATOR.strip()}"
        + f"{body.province}"
    )
    redis.rpush(
        RedisConfig.REDIS_SLEEP_GOOGLE_MAP_SEARCH_QUERIES, search_query
    )

    return {
        "imported_requests": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in imported_requests
        ]
        if imported_requests
        else [],
        "not_imported_requests": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in not_imported_requests
        ]
        if not_imported_requests
        else [],
        "in_processing_requests": in_processing_requests,
        "sleeped_search_requests": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in sleeped_search_requests
        ]
        if sleeped_search_requests
        else [],
        "in_queue_search_queries": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in in_queue_search_queries
        ] if in_queue_search_queries else [],
    }


@scrap_req_router.post(
    "/request_in_neshan_map", response_model=ResponseBody, status_code=200
)
async def request(body: RequestBody):
    """
    request search query to scrap in neshan map
    """
    sleeped_search_requests: list[str] = redis.lrange(
        name=RedisConfig.REDIS_SLEEP_NESHAN_SEARCH_QUERIES,
        start=0,
        end=-1,
    )
    in_queue_search_queries: list[str] = redis.lrange(
        name=RedisConfig.REDIS_INQUEUE_NESHAN_SEARCH_QUERIES,
        start=0,
        end=-1,
    )
    in_processing_requests: str = redis.get(
        RedisConfig.REDIS_NESHAN_IN_PROCESSING_SEARCH_QUERY
    )

    imported_requests = get_neshan_imported_requests()
    not_imported_requests = get_neshan_not_imported_requests()

    error_message = ""

    requested_search_query = (
        f"{body.listing_type.strip()}"
        + f"{AppConfig.SEARCH_QUERY_SEPARATOR.strip()}"
        + f"{body.verb.strip()}"
        + f"{AppConfig.SEARCH_QUERY_SEPARATOR.strip()}"
        + f"{body.city.strip()}"
    )
    clean_requested_search_query = (
        f"{body.listing_type.strip()}"
        + f" "
        + f"{body.verb.strip()}"
        + f" "
        + f"{body.city.strip()}"
    )

    if imported_requests:
        for imported_request in imported_requests:
            listing_category, listing_search_query, province, scraper = [
                i.strip()
                for i in imported_request.split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is imported to site under type of {listing_category}"

    if not_imported_requests:
        for not_imported_request in not_imported_requests:
            listing_category, listing_search_query, province, scraper = [
                i.strip()
                for i in not_imported_request.split(
                    AppConfig.LISTING_NAME_ITEMS_SEPARATOR
                )
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is scraped (but not imported to site) under type of {listing_category}"

    if sleeped_search_requests:
        for sleeped_request in sleeped_search_requests:
            listing_category, listing_search_query, province = [
                i.strip()
                for i in sleeped_request.split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is sleeped and waiting to enter on scraper queue under type of {listing_category}"
    if in_queue_search_queries:
        for in_queue_search_query in in_queue_search_queries:
            listing_category, listing_search_query, province = [
                i.strip()
                for i in in_queue_search_query.split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
            ]
            if requested_search_query == listing_search_query:
                error_message = f"request {clean_requested_search_query} is in scraper queue under type of {listing_category}"
        
    
    if in_processing_requests:
        listing_category, listing_search_query, province = [
            i.strip()
            for i in in_processing_requests.split(
                AppConfig.LISTING_NAME_ITEMS_SEPARATOR
            )
        ]
        if requested_search_query == listing_search_query:
            error_message = f"The {clean_requested_search_query} request is being scrapped. under type of {listing_category}"

    if error_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )

    search_query = (
        f"{body.listing_category.strip()}"
        + f"{AppConfig.LISTING_NAME_ITEMS_SEPARATOR.strip()}"
        + f"{requested_search_query}"
        + f"{AppConfig.LISTING_NAME_ITEMS_SEPARATOR.strip()}"
        + f"{body.province}"
    )
    redis.rpush(
        RedisConfig.REDIS_SLEEP_NESHAN_SEARCH_QUERIES, search_query
    )

    return {
        "imported_requests": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in imported_requests
        ]
        if imported_requests
        else [],
        "not_imported_requests": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in not_imported_requests
        ]
        if not_imported_requests
        else [],
        "in_processing_requests": in_processing_requests,
        "sleeped_search_requests": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in sleeped_search_requests
        ]
        if sleeped_search_requests
        else [],
        "in_queue_search_queries": [
            " ".join(i.split(AppConfig.SEARCH_QUERY_SEPARATOR))
            for i in in_queue_search_queries
        ] if in_queue_search_queries else [],
    }