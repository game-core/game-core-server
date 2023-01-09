from fastapi import APIRouter, Depends
from game_core_server.model.search_models import GamesSearchQuery
from game_core_server.service.search_games_service import SearchGamesService

router = APIRouter(prefix="/v1/games", tags=["search"])


@router.get("/search")
async def games_search(
    query: GamesSearchQuery = Depends(), handler: SearchGamesService = Depends()
):
    """
    Makes a search request to IGDB API.
    """
    return await handler.search_games(query)


