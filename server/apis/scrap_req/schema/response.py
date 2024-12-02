from pydantic import BaseModel, Field


class ResponseBody(BaseModel):
    imported_requests: list[str] = []
    not_imported_requests: list[str] = []
    in_processing_requests: str|None = None
    sleeped_search_requests: list[str] = []
    in_queue_search_queries: list[str] = []
