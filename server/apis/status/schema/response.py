from pydantic import BaseModel, Field

class ResponseBody(BaseModel):
    google_map_imported_requests: list[str] = []
    google_map_not_imported_requests: list[str] = []
    google_map_in_processing_requests: str|None = None
    google_map_sleeped_search_requests: list[str] = []
    google_map_in_queue_search_queries: list[str] = []
    neshan_imported_requests: list[str] = []
    neshan_not_imported_requests: list[str] = []
    neshan_in_processing_requests:str|None = None
    neshan_sleeped_search_requests: list[str] = []
    neshan_in_queue_search_queries: list[str] = []
