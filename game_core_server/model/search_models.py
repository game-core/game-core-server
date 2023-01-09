from fastapi import Query, Body
from pydantic import BaseModel


class GamesSearchQuery(BaseModel):
    """Class that defines the model of the search query."""

    search: str = Query(..., min_length=3, max_length=60)
    page: int = Query(default=1, ge=1)
