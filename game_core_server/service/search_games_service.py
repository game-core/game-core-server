from typing import Any, Dict
from fastapi import HTTPException, Depends
from gc_integrations.igdb import IGDBClient
from gc_integrations.igdb.models.auth_models import IGDBAuth
from game_core_server.model.search_models import GamesSearchQuery
from game_core_server.utils.renovate_tokens import get_current_igdb_token
from keys import gci_secrets
import re


class SearchGamesService:
    def __init__(self, igdb_token: IGDBAuth = Depends(get_current_igdb_token)):
        self.secrets = gci_secrets
        self.bearer_token = igdb_token.access_token
        self.client = IGDBClient(self.secrets.IGDB_CLIENT_ID, self.bearer_token)

    @staticmethod
    def _surround_search_query(search_query: str):
        """Surrounds the "search" paramater of GamesSearchQuery if the user has not already done so.

        Args:
            search_query (str): The search query to be surrounded.

        Returns:
            str: The surrounded search query.
        """
        quotes_regex = re.compile(r'((?<![\\])[\'"])((?:.(?!(?<![\\])\1))*.?)\1')
        if re.match(quotes_regex, search_query):
            return search_query
        else:
            return f'"{search_query}"'

    async def search_games(self, query: GamesSearchQuery):
        """Games Search Service main method"""
        normalized_query_dict: Dict[str, Any] = query.dict()
        normalized_query_dict.update(
            {"search": self._surround_search_query(query.search)}
        )
        request: list = await self.client.make_request("games", normalized_query_dict)
        if request is None or not bool(request):
            raise HTTPException(
                status_code=400, detail="No games found for the given query."
            )
        return request
